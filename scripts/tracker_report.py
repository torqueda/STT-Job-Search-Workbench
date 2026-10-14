#!/usr/bin/env python3
"""tracker_report.py: read-only cohort report for the weekly review.

Only applications at least --minimum-age-days old are compared, grouped by job family, source and fit.
A blank outcome means "no recorded outcome", never "rejected". The cohorts are small and not random, so no
causal claim about letters, resumes or sources can be drawn from these counts.
"""
import argparse
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracker import Tracker  # noqa: E402
from workspace import announce, load_config, workspace_dir  # noqa: E402


def summarize(rows, today, minimum_age=30):
    mature = [r for r in rows if r.get('date') and r['date'] <= today - timedelta(days=minimum_age)
              and not str(r.get('status') or '').startswith('Incomplete')]
    groups = {}
    for row in mature:
        key = (row.get('family') or 'Unknown family', row.get('source') or 'Unknown source', row.get('fit') or 'Unknown fit')
        counts = groups.setdefault(key, Counter())
        counts['applications'] += 1
        status = row.get('status') or ''
        if status == 'Offer' or 'Interview' in status:
            counts['recorded interview/offer outcomes'] += 1
        elif status == 'Rejected':
            counts['recorded rejection without interview detail'] += 1
        elif not status or status == 'Submitted':
            counts['no recorded outcome'] += 1
        else:
            counts['other recorded stage'] += 1
    return mature, groups


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--minimum-age-days', type=int, default=30)
    parser.add_argument('--as-of', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    cfg = load_config(ws)
    announce(cfg)
    rows = Tracker(cfg, ws).read()
    mature, groups = summarize(rows, datetime.strptime(args.as_of, '%Y-%m-%d'), args.minimum_age_days)
    print(f'{len(rows)} recorded applications; {len(mature)} at least {args.minimum_age_days} days old as of {args.as_of}.')
    for key, counts in sorted(groups.items()):
        print(' | '.join(key) + ': ' + str(dict(counts)))
    print('Small, nonrandom cohorts; unknown metadata stays unknown. No causal conclusion about letters, resumes '
          'or sources can be drawn from these counts.')


if __name__ == '__main__':
    main()
