#!/usr/bin/env python3
"""archive_handoff.py: keep HANDOFF.md short by moving older entries to history/.

The handoff log is read at the start of every session, so its length is a cost paid every time. This keeps the
newest entries (default: the newest 10) in HANDOFF.md and appends the rest, unchanged and in order, to
history/HANDOFF-through-<date>.md. Entries start with a line beginning "## ". Nothing is deleted.

Usage:
    python3 scripts/archive_handoff.py [--keep 10] [--workspace PATH] [--dry-run]
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace import workspace_dir  # noqa: E402


def split_entries(text):
    """(preamble, [entry, ...]) where each entry starts at a line beginning with '## '."""
    parts = re.split(r'(?m)^(?=## )', text)
    return parts[0], parts[1:]


def archive(ws, keep=10, dry_run=False):
    path = Path(ws) / 'HANDOFF.md'
    preamble, entries = split_entries(path.read_text(encoding='utf-8'))
    if len(entries) <= keep:
        return 0, None
    old = entries[keep:]
    target = Path(ws) / 'history' / f"HANDOFF-through-{datetime.now().strftime('%Y-%m-%d')}.md"
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('a', encoding='utf-8') as handle:
            handle.write(''.join(old))
        path.write_text(preamble + ''.join(entries[:keep]), encoding='utf-8')
    return len(old), target


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--keep', type=int, default=10)
    parser.add_argument('--workspace')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    moved, target = archive(workspace_dir(args.workspace), args.keep, args.dry_run)
    print(f'{"Would move" if args.dry_run else "Moved"} {moved} older entr{"y" if moved == 1 else "ies"}' + (f' to {target}' if target else '.'))


if __name__ == '__main__':
    main()
