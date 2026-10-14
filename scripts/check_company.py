#!/usr/bin/env python3
"""check_company.py: anti-duplicate and exclusion check, run before spending time on a posting.

Reads config.json and the tracker and applies these rules (see templates/APPLICATION_POLICY.md):

    Rule 1  company cap       at most N applications to one company inside a rolling window
    Rule 3  exact URL         the normalized posting URL is already in the tracker
    Rule 3b requisition       the same company and requisition ID is already in the tracker
    Rule 4  excluded company  listed in config.json "excluded_companies"

Incomplete attempts (status starting with "Incomplete") are not counted.

Usage:
    python3 scripts/check_company.py "Acme" [--url URL] [--requisition-id ID] [--days-threshold N] [--max-per-company N]

Prints OK (exit 0) or SKIP with the reason (exit 1).
"""
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracker import Tracker  # noqa: E402
from workspace import announce, load_config, workspace_dir  # noqa: E402

TRACKING_KEYS = {'source', 'src', 'ref', 'gh_src', 'iis', 'iisn'}


def normalize_url(url):
    """Drop tracking parameters and fragments, keep identifiers (job IDs) and sort what remains."""
    parts = urlsplit((url or '').strip())
    query = [(k, v) for k, v in parse_qsl(parts.query)
             if not k.lower().startswith('utm_') and k.lower() not in TRACKING_KEYS]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip('/'), urlencode(sorted(query)), ''))


def norm(value):
    return (value or '').strip().casefold()


def counted_rows(rows):
    """Rows that count toward caps and duplicate checks: everything except incomplete attempts."""
    return [r for r in rows if not str(r.get('status') or '').startswith('Incomplete')]


def excluded_names(cfg, now=None):
    """excluded_companies entries are plain names or {"name": ..., "reason": ..., "until": "YYYY-MM-DD"}."""
    names = set()
    as_of = (now or datetime.now()).date()
    for entry in cfg.get('excluded_companies', []):
        if isinstance(entry, dict):
            until = entry.get('until')
            if until and as_of > datetime.strptime(until, '%Y-%m-%d').date():
                continue
            names.add(norm(entry['name']))
        else:
            names.add(norm(entry))
    return names


def check(company, cfg, tracker, url=None, requisition_id=None, window_days=None, max_per_company=None, now=None):
    """Return (ok, message). `now` defaults to today; pass a date to reproduce a past or demo situation."""
    window_days = window_days or cfg.get('duplicate_check_days_threshold', 60)
    max_per_company = max_per_company or cfg.get('max_applications_per_company_in_window', 2)
    if norm(company) in excluded_names(cfg, now):
        return False, f"SKIP - Rule 4: '{company}' is in excluded_companies."
    rows = counted_rows(tracker.read())
    if url:
        for row in rows:
            if row['link'] and normalize_url(row['link']) == normalize_url(url):
                return False, f"SKIP - Rule 3: offer URL already in tracker (company '{row['company']}')."
    if requisition_id and any(norm(r['company']) == norm(company) and r['requisition_id'] == requisition_id for r in rows):
        return False, 'SKIP - Rule 3b: requisition already in tracker.'
    now = now or datetime.now()
    cutoff = now - timedelta(days=window_days)
    recent = [r for r in rows if norm(r['company']) == norm(company) and r['date'] and cutoff <= r['date'] <= now]
    if len(recent) >= max_per_company:
        dates = ', '.join(r['date'].strftime('%Y-%m-%d') for r in recent)
        return False, (f"SKIP - Rule 1: '{company}' already has {len(recent)} application(s) in the last "
                       f'{window_days} days (cap {max_per_company}). Dates: {dates}')
    return True, (f'OK - no duplicate found, can be applied. ({len(recent)} in last {window_days}d, '
                  f'{max_per_company - len(recent)} slot(s) left for this company.)')


def main():
    parser = argparse.ArgumentParser(description='Check whether a company/offer can be applied to.')
    parser.add_argument('company')
    parser.add_argument('--requisition-id')
    parser.add_argument('--url', help='Offer URL, enables the exact-match check')
    parser.add_argument('--days-threshold', type=int)
    parser.add_argument('--max-per-company', type=int)
    parser.add_argument('--as-of', help='YYYY-MM-DD: evaluate the window as of this date (default: today).')
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    cfg = load_config(ws)
    announce(cfg)
    ok, message = check(args.company, cfg, Tracker(cfg, ws), args.url, args.requisition_id,
                        args.days_threshold, args.max_per_company,
                        datetime.strptime(args.as_of, '%Y-%m-%d') if args.as_of else None)
    print(message)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
