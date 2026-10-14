#!/usr/bin/env python3
"""tracker_update.py: log a submitted application or update a stage in the tracker.

This script never submits anything. You (the person applying) submit every application; afterwards you tell
the assistant, and it runs this to record it.

New application (only after you confirm you submitted it):
    python3 scripts/tracker_update.py --title "Data Analyst" --company "Acme" --link https://... \\
        --requisition-id 1234 --date 2026-01-05 --confirmed-submitted --package workspace/application_packages/<dir>
    (--resume-spec <spec.json> may replace --package when the only artifact is a PDF you exported yourself)

Update an existing row:
    python3 scripts/tracker_update.py --update-row 7 --status Interview --stage-date 2026-01-20 --interview-date 2026-01-22
    python3 scripts/tracker_update.py --update-row 7 --status Rejected      # dated today unless --stage-date is given

Add --dry-run to preview the change without writing. Every real write backs the tracker up first, is atomic,
and appends an event to application_events.jsonl.

Rules enforced here (see templates/APPLICATION_POLICY.md):
    * a repeated normalized URL, or repeated company + requisition, is an error: update the existing row instead;
    * the per-company window cap is a WARNING, never a block: refusing the row would not un-send the application;
    * stage changes need the actual date (a rejection defaults to the day it is reported).
"""
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from application_package import verify_package  # noqa: E402
from check_company import counted_rows, normalize_url, norm  # noqa: E402
from tracker import Tracker, format_date  # noqa: E402
from workspace import announce, load_config, read_json, resolve, workspace_dir  # noqa: E402


def date_value(value):
    return datetime.strptime(value, '%Y-%m-%d') if value else None


def today():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def make_args(**overrides):
    """An args object with every option unset; handy for tests and for calling update() from Python."""
    base = dict(title=None, company=None, location=None, link=None, date=None, status=None, family=None, package=None,
                resume_spec=None, requisition_id=None, fit=None, source=None, stage_date=None, response_date=None,
                interview_date=None, next_action=None, jtype='Full-time', update_row=None, confirmed_submitted=False,
                dry_run=False)
    base.update(overrides)
    return argparse.Namespace(**base)


def resolve_resume_spec(path, company, ws):
    """Resume version of record, taken from the Gate 1 approved tailoring spec.

    Exported PDFs are usually renamed per role, so a filename is not a reliable identity. The spec that produced
    the resume is, and it has already been reviewed. A package is a stronger record and wins where one exists.
    """
    file = resolve(ws, path)
    spec = read_json(file)
    if spec.get('schema_version') != 2:
        raise ValueError('Resume spec must be schema_version 2.')
    if not spec.get('approved'):
        raise ValueError('Resume spec is not Gate 1 approved.')
    matches = [v for v in spec.get('versions', []) if any(norm(c) == norm(company) for c in v.get('companies', []))]
    if not matches:
        raise ValueError(f'No version in {file.name} lists {company}. Record the company in the spec that produced its resume.')
    if len(matches) > 1:
        raise ValueError(f'{company} appears in more than one version of {file.name}; resolve the spec before logging.')
    version = matches[0]
    label = version.get('label') or version['canonical_id']
    return {'resume_version': label, 'family': version.get('job_family'),
            'note': f'No package - resume version {label} from {file.name} (Gate 1 approved). '
                    'Final PDF exported manually; filename not tracked.'}


def _stage_update(args, rows):
    row = next((r for r in rows if r['_row'] == args.update_row), None)
    if row is None:
        raise ValueError('Update row is not an existing application.')
    if not any((args.status, args.next_action, args.response_date, args.interview_date)):
        raise ValueError('Provide a stage, next action or actual event date.')
    stage_date = date_value(args.stage_date)
    response_date = args.response_date
    # A rejection is recorded on the day it is reported. Every other stage change needs its actual --stage-date.
    if args.status and not stage_date and 'rejected' in args.status.casefold():
        stage_date = today()
        if response_date is None and not row['response_date']:
            response_date = stage_date.strftime('%Y-%m-%d')
    if args.status and not stage_date:
        raise ValueError('Stage changes require the actual --stage-date.')
    changes = {}
    if args.status:
        changes.update(status=args.status, stage_date=stage_date)
    if args.next_action is not None:
        changes['next_action'] = args.next_action
    if response_date is not None:
        changes['response_date'] = date_value(response_date)
    if args.interview_date is not None:
        changes['interview_date'] = date_value(args.interview_date)
    return [('update', args.update_row, changes)], row, {**row, **changes}, []


def _new_application(args, cfg, rows, ws):
    status = args.status or 'Submitted'
    incomplete = status.startswith('Incomplete')
    if not incomplete and not args.confirmed_submitted:
        raise ValueError('Log only after you confirm submission; pass --confirmed-submitted.')
    if not incomplete and not args.date:
        raise ValueError('Record the actual submission date with --date YYYY-MM-DD; do not assume today.')
    package = verify_package(args.package) if args.package else {}

    def choose(field, supplied):
        if supplied and package.get(field) and supplied != package[field]:
            raise ValueError(f'{field} conflicts with package.')
        return supplied or package.get(field)

    title = choose('title', args.title)
    company = choose('company', args.company)
    url = choose('url', args.link)
    spec = resolve_resume_spec(args.resume_spec, company, ws) if args.resume_spec else {}
    if not incomplete and not package and not spec:
        raise ValueError('New submissions require --package, or --resume-spec naming the approved schema-v2 tailoring '
                         'spec whose version covers this company.')
    if not title or not company or not url:
        raise ValueError('Title, company and URL are required.')
    when = date_value(args.date) or today()
    cap_warnings = []
    if not incomplete:
        submitted = counted_rows(rows)
        if any(r['link'] and normalize_url(r['link']) == normalize_url(url) for r in submitted):
            raise ValueError('URL already recorded; use --update-row.')
        requisition = package.get('requisition_id') or args.requisition_id
        if requisition and any(norm(r['company']) == norm(company) and r['requisition_id'] == requisition for r in submitted):
            raise ValueError('Company/requisition already recorded.')
        window_days = cfg.get('duplicate_check_days_threshold', 60)
        in_window = [r for r in submitted if norm(r['company']) == norm(company) and r['date']
                     and when - timedelta(days=window_days) <= r['date'] <= when]
        cap = cfg.get('max_applications_per_company_in_window')
        if cap is not None and len(in_window) >= cap:
            cap_warnings.append(f'Company cap exceeded: {len(in_window)} application(s) to {company} already recorded '
                                f'within {window_days} days (limit {cap}).')
    values = {
        'date': when, 'company': company, 'job_title': title, 'type': args.jtype,
        'location': args.location or package.get('location', ''), 'link': url,
        'requisition_id': package.get('requisition_id') or args.requisition_id,
        'family': package.get('family') or spec.get('family') or args.family,
        'fit': package.get('fit') or args.fit, 'source': package.get('source') or args.source,
        'referral': package.get('referral'),
        'resume_version': package.get('resume_version') or spec.get('resume_version'),
        'package': str(Path(args.package).resolve()) if args.package else spec.get('note'),
        'status': status, 'stage_date': date_value(args.stage_date) or when,
        'response_date': date_value(args.response_date), 'interview_date': date_value(args.interview_date),
        'next_action': args.next_action,
    }
    return [('append', values)], {}, values, cap_warnings


def update(args, cfg, ws=None):
    ws = workspace_dir(ws)
    tracker = Tracker(cfg, ws)
    rows = tracker.read()
    operations, before, after, cap_warnings = (_stage_update(args, rows) if args.update_row
                                               else _new_application(args, cfg, rows, ws))
    event = {'recorded_at': datetime.now().isoformat(), 'tracker': str(tracker.path),
             'before': {k: format_date(v) if isinstance(v, datetime) else v for k, v in before.items()},
             'after': {k: format_date(v) if isinstance(v, datetime) else v for k, v in after.items()}}
    if cap_warnings:
        event['cap_warnings'] = cap_warnings
    if args.dry_run:
        return {'dry_run': True, 'event': event, 'cap_warnings': cap_warnings}
    touched, backup = tracker.apply(operations)
    event['row'] = touched[0]
    events = resolve(ws, cfg.get('events_path', 'application_events.jsonl'))
    try:
        with events.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(event, default=str) + '\n')
    except OSError as exc:
        recovery = tracker.path.with_name(tracker.path.name + '.pending-event.json')
        recovery.write_text(json.dumps(event, default=str, indent=2))
        raise ValueError(f'Tracker saved but the event append failed: {exc}. Event preserved in {recovery}; do not append again.')
    return {'row': touched[0], 'backup': str(backup) if backup else None, 'event': event, 'cap_warnings': cap_warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    for key in ('title', 'company', 'location', 'link', 'date', 'status', 'family', 'package', 'resume-spec',
                'requisition-id', 'fit', 'source', 'stage-date', 'response-date', 'interview-date', 'next-action'):
        parser.add_argument('--' + key)
    parser.add_argument('--type', default='Full-time', dest='jtype')
    parser.add_argument('--update-row', type=int)
    parser.add_argument('--confirmed-submitted', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    cfg = load_config(ws)
    announce(cfg)
    try:
        result = update(args, cfg, ws)
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit(str(exc))
    for warning in result.get('cap_warnings') or []:
        print('PLANNING CAP WARNING: ' + warning, file=sys.stderr)
    print(json.dumps(result, default=str, indent=2))


if __name__ == '__main__':
    main()
