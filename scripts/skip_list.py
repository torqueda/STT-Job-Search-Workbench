#!/usr/bin/env python3
"""skip_list.py: persistent record of listings triaged and rejected at Gate 1.

Triage takes real review time, and aggregators do not reliably keep out-of-range postings out of a search.
Without this file the same rejected posting resurfaces in a later batch and costs review time twice.

The skip list is separate from the tracker on purpose: the tracker records real applications (after the user
submits), and a Gate 1 rejection is not an application, so it must not count toward any company cap. This is
an append-only log matched by exact apply URL, consumed by sourcing.py.

Usage:
    python3 scripts/skip_list.py add --url "https://..." --title "Data Analyst" --company "Acme" \\
        --role-profile data_analytics --batch 2026-01-05 --reason "Requires 5+ years"
    python3 scripts/skip_list.py list [--role-profile data_analytics]
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace import announce, load_config_or_empty, workspace_dir  # noqa: E402


def default_path(ws=None):
    return workspace_dir(ws) / 'skipped_listings.json'


def load_entries(path):
    path = Path(path)
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else []


def load_skipped_urls(path):
    return {e['url'] for e in load_entries(path) if e.get('url')}


def save_entries(entries, path):
    Path(path).write_text(json.dumps(entries, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def add_entry(path, url, reason, title='', company='', role_profile='', batch='', date=None):
    """Append one skipped listing. Returns False if the URL was already recorded."""
    entries = load_entries(path)
    if any(e.get('url') == url for e in entries):
        return False
    entries.append({'url': url, 'title': title or '', 'company': company or '', 'role_profile': role_profile or '',
                    'batch': batch or '', 'date_skipped': date or datetime.now().strftime('%Y-%m-%d'), 'reason': reason})
    save_entries(entries, path)
    return True


def main():
    parser = argparse.ArgumentParser(description='Track Gate-1-rejected listings so they are not suggested again.')
    parser.add_argument('--workspace')
    parser.add_argument('--file')
    sub = parser.add_subparsers(dest='cmd', required=True)
    add = sub.add_parser('add', help='Log one rejected listing.')
    add.add_argument('--url', required=True)
    add.add_argument('--title')
    add.add_argument('--company')
    add.add_argument('--role-profile')
    add.add_argument('--batch')
    add.add_argument('--date', help='YYYY-MM-DD (default: today)')
    add.add_argument('--reason', required=True, help="Why it was rejected, e.g. 'requires 5+ years'")
    listing = sub.add_parser('list', help='Show accumulated entries.')
    listing.add_argument('--role-profile')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    announce(load_config_or_empty(ws))
    path = args.file or default_path(ws)
    if args.cmd == 'add':
        if add_entry(path, args.url, args.reason, args.title, args.company, args.role_profile, args.batch, args.date):
            print(f"Added to skip list: {args.title or '(untitled)'} - {args.company or '?'}\n  reason: {args.reason}")
        else:
            print(f'Already in skip list, not re-added: {args.url}')
        return
    entries = load_entries(path)
    if args.role_profile:
        entries = [e for e in entries if e.get('role_profile') == args.role_profile]
    if not entries:
        print('Skip list is empty.')
        return
    print(f'{len(entries)} skipped listing(s):')
    for e in entries:
        print(f"  [{e.get('date_skipped', '?')}] {e.get('title', '?')} - {e.get('company', '?')}  ({e.get('role_profile', '?')})")
        print(f"      reason: {e.get('reason', '?')}\n      url: {e.get('url', '?')}")


if __name__ == '__main__':
    main()
