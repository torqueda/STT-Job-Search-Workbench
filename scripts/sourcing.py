#!/usr/bin/env python3
"""sourcing.py: turn a feed of postings into a dated batch file for triage.

Sources (all open or user-supplied; nothing here logs in to any site):

  github  a public JSON listings feed on GitHub (default: the URL in config.json "sources.github_feed_url").
          Rows are expected to carry company_name, title, url, locations, date_posted (unix seconds), active,
          is_visible, and optionally category, degrees, sponsorship.
  file    the same JSON shape from a local file (--infile), for a feed you saved or another agent produced.
  manual  text you paste: one block per posting separated by a line containing only "===". The first line is
          the title, the second the company, the third the location; any line starting with http is the URL.

Filters from config.json: excluded_companies, excluded_keywords, excluded_title_patterns (regexes tested against
the title, e.g. a seniority word at the START of a title), and lane_title_patterns (for feeds: a title must match
one). Rows already in the tracker (normalized URL) or in the skip list are dropped and counted separately.
Deduplicating by company cap is a separate step: run check_company.py per posting you pursue.

Output: <workspace>/batches/YYYY-MM-DD_<role_profile>.md in the numbered format prompts/05_triage.md expects.

Usage:
    python3 scripts/sourcing.py --role-profile data_analytics --source github --hours 24
    python3 scripts/sourcing.py --role-profile data_analytics --source manual --infile my_postings.txt
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_company import excluded_names, normalize_url  # noqa: E402
from skip_list import default_path, load_skipped_urls  # noqa: E402
from tracker import Tracker  # noqa: E402
from workspace import announce, load_config, workspace_dir  # noqa: E402

USER_AGENT = 'STT-Job-Search-Workbench/1.0 (+https://github.com/torqueda/STT-Job-Search-Workbench; personal job search; reads public JSON)'


def http_get_json(url, timeout=60):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode('utf-8', 'replace'))


def listing_from_feed_row(row):
    """Map one feed row to the common listing shape."""
    locations = row.get('locations') or []
    location = '; '.join(locations) if isinstance(locations, list) else str(locations)
    details = []
    for label, key in (('Category', 'category'), ('Degrees', 'degrees'), ('Sponsorship', 'sponsorship')):
        value = row.get(key)
        if value:
            details.append(f"{label}: {', '.join(value) if isinstance(value, list) else value}")
    description = '\n'.join(details + ['(Full description not included in the feed; open the URL.)'])
    return {'title': (row.get('title') or 'Unknown title').strip(), 'company': (row.get('company_name') or 'Unknown company').strip(),
            'location': location, 'url': (row.get('url') or '').strip(), 'description': description,
            'posted': row.get('date_posted')}


def fetch_feed(rows, hours=None, now=None):
    """Active, visible rows, optionally only those posted in the last `hours` hours."""
    now = now or time.time()
    out = []
    for row in rows:
        if row.get('active') is False or row.get('is_visible') is False:
            continue
        if hours and (not row.get('date_posted') or now - row['date_posted'] > hours * 3600):
            continue
        out.append(listing_from_feed_row(row))
    return out


def parse_manual(text):
    listings = []
    for block in re.split(r'^\s*===\s*$', text, flags=re.MULTILINE):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        listings.append({'title': lines[0], 'company': lines[1] if len(lines) > 1 else 'Unknown company',
                         'location': lines[2] if len(lines) > 2 else '',
                         'url': next((l for l in lines if l.lower().startswith('http')), ''),
                         'description': block.strip(), 'posted': None})
    return listings


def apply_filters(listings, cfg, skip_urls=None, applied_urls=None, use_lane=False):
    """Return (kept, dropped_by_filters, skipped_before, already_applied). Reasons stay distinguishable in the summary."""
    excluded_companies = excluded_names(cfg)
    excluded_keywords = [k.strip().casefold() for k in cfg.get('excluded_keywords', [])]
    title_patterns = cfg.get('excluded_title_patterns', [])
    lane_patterns = cfg.get('lane_title_patterns', []) if use_lane else []
    skip_urls = skip_urls or set()
    applied = {normalize_url(u) for u in (applied_urls or set())}
    kept, dropped, skipped, already = [], 0, 0, 0
    for listing in listings:
        if listing['url'] and normalize_url(listing['url']) in applied:
            already += 1
        elif listing['url'] and listing['url'] in skip_urls:
            skipped += 1
        elif listing['company'].strip().casefold() in excluded_companies:
            dropped += 1
        elif any(k in f"{listing['title']} {listing['description']}".casefold() for k in excluded_keywords):
            dropped += 1
        elif any(re.search(p, listing['title'], re.I) for p in title_patterns):
            dropped += 1
        elif lane_patterns and not any(re.search(p, listing['title'], re.I) for p in lane_patterns):
            dropped += 1
        else:
            kept.append(listing)
    return kept, dropped, skipped, already


def write_batch(listings, role_profile, query, batch_dir):
    """Preserve earlier batches, including repeat queries, with a _2, _3 suffix."""
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', role_profile):
        raise ValueError('Role profile must be a filename label using letters, numbers, underscores or hyphens.')
    batch_dir = Path(batch_dir)
    batch_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y-%m-%d')
    path = batch_dir / f'{stamp}_{role_profile}.md'
    n = 1
    while path.exists():
        n += 1
        path = batch_dir / f'{stamp}_{role_profile}_{n}.md'
    lines = [f'# Postings batch - {stamp}', f'Role profile: {role_profile}  |  Query: {query}  |  Count: {len(listings)}', '',
             'Hand this file to the assistant for triage (prompts/05_triage.md).', '', '---', '']
    for i, listing in enumerate(listings, 1):
        lines += [f"## Posting {i}: {listing['title']} - {listing['company']}",
                  f"- Location: {listing['location'] or 'N/A'}", f"- URL: {listing['url'] or 'N/A'}", '',
                  'Description:', listing['description'] or '(no description captured; open the URL)', '', '---', '']
    with path.open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines))
    return path


def main():
    parser = argparse.ArgumentParser(description='Source postings into a dated batch file.')
    parser.add_argument('--role-profile', required=True, help='A short label for this batch, e.g. data_analytics.')
    parser.add_argument('--source', choices=['github', 'file', 'manual'], default='github')
    parser.add_argument('--infile', help='file source: JSON feed file. manual source: text blocks separated by ===.')
    parser.add_argument('--query', help='Label recorded in the batch header (default: the role profile).')
    parser.add_argument('--hours', type=int, help='Feeds: keep rows posted within this many hours.')
    parser.add_argument('--limit', type=int, default=0, help='Keep at most this many listings (0 = no cap).')
    parser.add_argument('--workspace')
    args = parser.parse_args()

    ws = workspace_dir(args.workspace)
    cfg = load_config(ws)
    announce(cfg)
    if args.source == 'manual':
        if not args.infile:
            sys.exit('manual source needs --infile (blocks separated by a line with ===).')
        listings = parse_manual(Path(args.infile).read_text(encoding='utf-8'))
    elif args.source == 'file':
        if not args.infile:
            sys.exit('file source needs --infile.')
        listings = fetch_feed(json.loads(Path(args.infile).read_text(encoding='utf-8')), args.hours)
    else:
        url = (cfg.get('sources') or {}).get('github_feed_url')
        if not url:
            sys.exit('No sources.github_feed_url in config.json. See docs/SOURCING.md.')
        try:
            listings = fetch_feed(http_get_json(url), args.hours)
        except OSError as exc:
            sys.exit(f'Could not read the feed: {exc}. Use --source file or --source manual.')
    skip_urls = load_skipped_urls(default_path(ws))
    applied_urls = {r['link'] for r in Tracker(cfg, ws).read()
                    if r['link'] and not str(r.get('status') or '').startswith('Incomplete')}
    kept, dropped, skipped, already = apply_filters(listings, cfg, skip_urls, applied_urls, use_lane=args.source != 'manual')
    kept = kept[:args.limit] if args.limit else kept
    path = write_batch(kept, args.role_profile, args.query or args.role_profile, ws / 'batches')
    print(f'Read {len(listings)} | dropped {dropped} by filters | {already} already in tracker | '
          f'{skipped} previously skipped at Gate 1 | wrote {len(kept)} listings.')
    print(f'Batch file: {path}')
    print('Next: verify the list is what you wanted, then ask the assistant to triage it.')


if __name__ == '__main__':
    main()
