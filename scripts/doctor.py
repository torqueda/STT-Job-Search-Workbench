#!/usr/bin/env python3
"""doctor.py: check that a workspace is complete and internally consistent.

Run it after the setup conversation, after any edit to the evidence ledger or persona profiles, and whenever a
script reports something odd. It reads only; it never changes a file.

Errors mean a generator would fail or produce unreliable output. Warnings mean the workspace works but a
control is switched off (for example no project aliases, so the storytelling check cannot recognise projects).

Usage:
    python3 scripts/doctor.py [--workspace PATH]
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracker import Tracker  # noqa: E402
from workspace import announce, load_config, read_json, workspace_dir  # noqa: E402

REQUIRED_FILES = ['config.json', 'base_resume.json', 'canonical_resumes.json', 'evidence/claims.json',
                  'PROFILE_AND_RULES.md']
RECOMMENDED_FILES = ['VOICE.md', 'APPLICATION_POLICY.md', 'HANDOFF.md', 'evidence/BOUNDARIES.md',
                     'evidence/known_errors.json', 'evidence/project_aliases.json']


def _load(ws, relative, errors):
    try:
        return read_json(ws / relative)
    except (OSError, ValueError) as exc:
        errors.append(f'{relative} cannot be read as JSON: {exc}')
        return None


def _check_regexes(patterns, where, errors):
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as exc:
            errors.append(f'{where}: invalid regex {pattern!r} ({exc})')


def diagnose(ws):
    ws = Path(ws)
    errors, warnings = [], []
    for relative in REQUIRED_FILES:
        if not (ws / relative).is_file():
            errors.append(f'Missing required file: {relative}')
    for relative in RECOMMENDED_FILES:
        if not (ws / relative).is_file():
            warnings.append(f'Missing recommended file: {relative}')
    if errors and not (ws / 'evidence/claims.json').is_file():
        return errors, warnings

    cfg = _load(ws, 'config.json', errors) or {}
    for field in ('excluded_title_patterns', 'lane_title_patterns'):
        _check_regexes(cfg.get(field, []), f'config.{field}', errors)
    _check_regexes((cfg.get('watch_filters') or {}).values(), 'config.watch_filters', errors)
    if (ws / 'employer_watchlist.json').is_file():
        watchlist = _load(ws, 'employer_watchlist.json', errors) or {}
        _check_regexes((watchlist.get('metros') or {}).values(), 'employer_watchlist.metros', errors)
    ledger = _load(ws, 'evidence/claims.json', errors) or {}
    catalog = _load(ws, 'canonical_resumes.json', errors) or {}
    claims = ledger.get('claims', {})
    if not ledger.get('revision'):
        errors.append('evidence/claims.json has no "revision".')
    if not claims:
        warnings.append('The evidence ledger has no claims yet. Resumes cannot be generated until the evidence '
                        'interview has produced some (prompts/02_evidence_builder.md).')
    for claim_id, claim in claims.items():
        if claim.get('status') == 'usable':
            for field in ('text', 'source', 'ownership', 'limitations'):
                if not claim.get(field):
                    warnings.append(f'Claim {claim_id} is usable but has no {field}.')

    base = _load(ws, 'base_resume.json', errors) if (ws / 'base_resume.json').is_file() else None
    if base:
        if str(base.get('name', '')).startswith('YOUR '):
            warnings.append('base_resume.json still holds the template placeholders (name, contact line, education).')
        usable = {' '.join(c['text'].split()) for c in claims.values() if c.get('status') == 'usable' and c.get('text')}
        for role in base.get('professional_experience', []):
            for bullet in role.get('bullets', []):
                if ' '.join(bullet.split()) not in usable:
                    warnings.append(f'base_resume.json bullet is not a usable ledger claim (every resume line must be): "{bullet[:60]}..."')

    if not catalog.get('revision'):
        errors.append('canonical_resumes.json has no "revision".')
    profiles = catalog.get('profiles', {})
    if not profiles:
        warnings.append('No persona profiles yet (prompts/03_personas_and_resumes.md creates them).')
    for name, profile in profiles.items():
        if profile.get('status') == 'retired':
            continue
        if not profile.get('family') or not profile.get('core_positioning'):
            errors.append(f'Profile {name} needs "family" and "core_positioning".')
        used = []
        for project in profile.get('projects', []):
            refs = list(project.get('claim_ids', []))
            if project.get('purpose_id'):
                refs.append(project['purpose_id'])
            else:
                warnings.append(f'Profile {name}, project {project.get("id")}: no purpose_id (the line that says why it existed).')
            for ref in refs:
                if ref not in claims:
                    errors.append(f'Profile {name} references unknown claim {ref}.')
                elif claims[ref].get('status') != 'usable':
                    errors.append(f'Profile {name} references claim {ref}, which is not usable.')
            used += refs
        missing = set(profile.get('required_claim_ids', [])) - set(used)
        if missing:
            errors.append(f'Profile {name} lists required claims it does not use: {sorted(missing)}')

    known = _load(ws, 'evidence/known_errors.json', errors) if (ws / 'evidence/known_errors.json').is_file() else {}
    for rule in (known or {}).get('rules', []):
        _check_regexes([p for p in (rule.get('pattern'), rule.get('unless')) if p], f'known_errors {rule.get("id", "?")}', errors)
        if not rule.get('message'):
            errors.append(f'known_errors {rule.get("id", "?")} needs a message.')
    aliases = _load(ws, 'evidence/project_aliases.json', errors) if (ws / 'evidence/project_aliases.json').is_file() else {}
    aliases = aliases or {}
    _check_regexes(aliases.get('projects', {}).values(), 'project_aliases', errors)
    if profiles and not aliases.get('projects'):
        warnings.append('No project aliases registered: the storytelling check cannot tell when an answer names a '
                        'project without introducing it. Add each project name to evidence/project_aliases.json.')

    try:
        tracker = Tracker(cfg, ws)
        tracker.read()
    except Exception as exc:  # any tracker misconfiguration is an error worth showing
        errors.append(f'Tracker unreadable: {exc}')
    else:
        if not tracker.path.exists():
            warnings.append('The tracker file does not exist yet; it is created when the first application is logged.')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    if not ws.is_dir():
        sys.exit(f'No workspace at {ws}. Run: python3 scripts/init_workspace.py')
    try:
        announce(load_config(ws))
    except Exception:
        pass
    errors, warnings = diagnose(ws)
    for message in errors:
        print(f'ERROR   {message}')
    for message in warnings:
        print(f'warning {message}')
    print(f'\n{len(errors)} error(s), {len(warnings)} warning(s) in {ws}')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
