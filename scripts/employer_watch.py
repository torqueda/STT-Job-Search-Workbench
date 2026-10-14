#!/usr/bin/env python3
"""employer_watch.py: read target employers' own public job boards for new postings.

For each employer in <workspace>/employer_watchlist.json, read the posting list straight from the employer's
applicant-tracking system through the public job-board endpoints those systems publish for exactly this kind of
reading, keep postings that are recent, in a metro you listed (or remote in the U.S.), and whose title fits the
lanes you set, then drop anything already in the tracker, the skip list or a recent batch file.

Adapters included:
    greenhouse   https://boards-api.greenhouse.io/v1/boards/<token>/jobs     (the board token is in the careers URL)
    lever        https://api.lever.co/v0/postings/<token>?mode=json
    manual       no public feed; listed once so the gap stays visible. Ask your assistant to add an adapter
                 for another system (see docs/SOURCING.md); keep requests few and gentle.

Read-only: plain GET requests, one employer at a time with a short pause. No login, no cookies.

Usage:
    python3 scripts/employer_watch.py --days 2
    python3 scripts/employer_watch.py --days 30 --out workspace/batches/watch_catchup.json

Filters come from config.json "watch_filters": lane (title must match), off_lane (title must not), level (title
must not, unless keep_despite_level matches) and remote_pattern. Metro patterns live in the watchlist file.
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_company import excluded_names, normalize_url, norm  # noqa: E402
from skip_list import default_path, load_skipped_urls  # noqa: E402
from tracker import Tracker  # noqa: E402
from workspace import announce, load_config, read_json, workspace_dir  # noqa: E402

USER_AGENT = 'STT-Job-Search-Workbench/1.0 (+https://github.com/torqueda/STT-Job-Search-Workbench; personal job search; reads public job-board JSON)'
DEFAULT_FILTERS = {
    'lane': r'data|analy|\bai\b|machine learning|\bml\b|automation|software|developer|engineer|product|scien|insight',
    'off_lane': r'intern\b|internship|nurse|driver|warehouse|cashier|sales|accountant|recruit|technician',
    'level': r'\b(senior|sr\.?|staff|principal|lead|director|manager|head of|vp|vice president|chief)\b',
    'keep_despite_level': r'\bassociate product manager\b|\bapm\b',
    'remote_pattern': r'\bremote\b',
}


def http_json(url, timeout=30):
    """One request only; the caller reports failures and moves to the next employer."""
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode('utf-8', 'replace'))


def parse_iso(value):
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


# Each adapter returns [{title, loc, posted (aware datetime or None), url, id, date_source}].

def adapter_greenhouse(employer, fetch=http_json):
    data = fetch(f"https://boards-api.greenhouse.io/v1/boards/{employer['token']}/jobs")
    out = []
    for job in data.get('jobs', []):
        stamp = job.get('first_published') or job.get('updated_at')
        out.append({'title': job.get('title'), 'loc': (job.get('location') or {}).get('name', ''),
                    'posted': parse_iso(stamp), 'url': job.get('absolute_url'),
                    'id': str(job.get('requisition_id') or job.get('id') or ''),
                    'date_source': 'first_published' if job.get('first_published') else 'updated_at (may be a later edit)'})
    return out


def adapter_lever(employer, fetch=http_json):
    data = fetch(f"https://api.lever.co/v0/postings/{employer['token']}?mode=json")
    out = []
    for job in data:
        created = job.get('createdAt')
        posted = dt.datetime.fromtimestamp(created / 1000, dt.timezone.utc) if created else None
        out.append({'title': job.get('text'), 'loc': (job.get('categories') or {}).get('location', ''), 'posted': posted,
                    'url': job.get('hostedUrl'), 'id': str(job.get('id') or ''), 'date_source': 'createdAt'})
    return out


ADAPTERS = {'greenhouse': adapter_greenhouse, 'lever': adapter_lever}


def keep(job, metro_regex, filters, days, now):
    """Why a posting is kept or dropped is decided here; returns (keep, reason)."""
    title = job.get('title') or ''
    if not re.search(filters['lane'], title, re.I):
        return False, 'off lane'
    if re.search(filters['off_lane'], title, re.I):
        return False, 'off lane'
    if re.search(filters['level'], title, re.I) and not (filters.get('keep_despite_level') and re.search(filters['keep_despite_level'], title, re.I)):
        return False, 'level'
    location = job.get('loc') or ''
    if not (re.search(filters['remote_pattern'], location, re.I) or (metro_regex and re.search(metro_regex, location))):
        return False, 'location'
    posted = job.get('posted')
    if posted is None or (now - posted).total_seconds() / 86400 > days:
        return False, 'age'
    return True, ''


def recent_batch_urls(ws):
    urls = set()
    for file in Path(ws, 'batches').glob('*.md') if Path(ws, 'batches').exists() else []:
        urls.update(normalize_url(u) for u in re.findall(r'https?://\S+', file.read_text(encoding='utf-8', errors='replace')))
    return urls


def watch(ws, cfg, days, fetchers=None, now=None, pause=0.5):
    now = now or dt.datetime.now(dt.timezone.utc)
    watchlist = read_json(Path(ws) / 'employer_watchlist.json')
    filters = {**DEFAULT_FILTERS, **(cfg.get('watch_filters') or {})}
    adapters = {**ADAPTERS, **(fetchers or {})}
    known = {normalize_url(r['link']) for r in Tracker(cfg, ws).read() if r['link']}
    known |= {normalize_url(u) for u in load_skipped_urls(default_path(ws))} | recent_batch_urls(ws)
    candidates, statuses = [], []
    excluded = excluded_names(cfg, now)
    for employer in watchlist.get('employers', []):
        name, kind = employer['name'], employer.get('ats', 'manual')
        if norm(name) in excluded:
            statuses.append({'employer': name, 'status': 'excluded'})
            continue
        if kind not in adapters:
            statuses.append({'employer': name, 'status': 'manual' if kind == 'manual' else f'no adapter for {kind}',
                             'note': employer.get('note', '')})
            continue
        try:
            jobs = adapters[kind](employer)
        except Exception as exc:  # report and continue; one employer's outage must not stop the run
            statuses.append({'employer': name, 'status': f'error: {exc}'})
            continue
        metro_regex = (watchlist.get('metros') or {}).get(employer.get('metro'))
        kept = 0
        for job in jobs:
            ok, _ = keep(job, metro_regex, filters, days, now)
            if ok and normalize_url(job['url'] or '') not in known:
                candidates.append({'employer': name, 'title': job['title'], 'location': job['loc'],
                                   'posted': job['posted'].date().isoformat(), 'date_source': job['date_source'],
                                   'url': job['url'], 'id': job['id']})
                kept += 1
        statuses.append({'employer': name, 'status': 'ok', 'read': len(jobs), 'candidates': kept})
        time.sleep(pause)
    return candidates, statuses


def main():
    parser = argparse.ArgumentParser(description='Read target employers\' public job boards for new postings.')
    parser.add_argument('--days', type=int, default=2)
    parser.add_argument('--out', help='Write the result JSON here (default: print a summary only).')
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    cfg = load_config(ws)
    announce(cfg)
    if not (ws / 'employer_watchlist.json').is_file():
        sys.exit('No employer_watchlist.json in the workspace. Copy templates/employer_watchlist.json and add employers.')
    candidates, statuses = watch(ws, cfg, args.days)
    result = {'days': args.days, 'candidates': candidates, 'employers': statuses}
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    for status in statuses:
        print(f"{status['employer']}: {status['status']}")
    print(f'\n{len(candidates)} candidate posting(s) in the last {args.days} day(s).')
    for c in candidates:
        print(f"  {c['employer']} | {c['title']} | {c['location']} | {c['posted']} | {c['url']}")
    print('Candidates are leads: read the full posting at the employer before triage.')


if __name__ == '__main__':
    main()
