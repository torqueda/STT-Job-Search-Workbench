#!/usr/bin/env python3
"""application_package.py: archive the exact reviewed files for one application.

A package freezes what was actually submitted: the final resume (and letter, if any), the saved job
description and the review of each file, with a SHA-256 for every file. Nothing is submitted, no network is
used and the tracker is not touched. `--verify` later proves the files have not changed.

Packaging refuses when:
    * the fit was not approved at Gate 1, or the three responsibility-to-evidence mappings are missing;
    * a file's review is missing, stale (text changed since review) or has unresolved warnings;
    * a resume or letter PDF/DOCX lacks a recorded page count and visual review, or a resume exceeds its page limit;
    * the destination already exists (submitted records are never overwritten).

Usage:
    python3 scripts/application_package.py --spec package_spec.json
    python3 scripts/application_package.py --verify workspace/application_packages/2026-01-05_Acme_1234
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workflow_quality import read_document, validate_review  # noqa: E402
from workspace import announce, load_config_or_empty, read_json, resolve, workspace_dir  # noqa: E402

REQUIRED = ('company', 'title', 'requisition_id', 'url', 'family', 'fit', 'source', 'resume_version', 'date',
            'jd_file', 'attachments')


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe(value):
    return re.sub(r'[^A-Za-z0-9_-]+', '_', value).strip('_') or 'unknown'


def verify_package(path):
    path = Path(path).resolve()
    manifest = read_json(path / 'manifest.json')
    for item in manifest['files']:
        file = (path / item['archive_name']).resolve()
        if file.parent != path or not file.is_file() or file_digest(file) != item['sha256']:
            raise ValueError(f"Package file changed or missing: {item['archive_name']}")
    return manifest


def _check_attachment(item, ws):
    path = Path(item['path'])
    if not path.is_file():
        raise ValueError(f'Missing attachment: {path}')
    review = read_json(item['review_file'])
    is_resume = item['kind'] == 'resume'
    errors, _ = validate_review(read_document(path), review, require_company=not is_resume, writing=not is_resume, ws=ws)
    if path.suffix.lower() in ('.pdf', '.docx'):
        pages = review.get('page_count')
        if not review.get('visual_review') or not isinstance(pages, int) or pages < 1:
            errors.append('Record actual rendered page count and visual review.')
        elif is_resume:
            limit = load_config_or_empty(ws).get('resume_limits', {}).get('max_pages', 1)
            if pages > limit:
                errors.append(f'Final resume exceeds the configured page limit ({limit}).')
    if errors:
        raise ValueError(f'{path}: ' + '; '.join(errors))


def prepare(spec, output_root, ws=None):
    ws = workspace_dir(ws)
    for key in REQUIRED:
        if not spec.get(key):
            raise ValueError(f'Missing package field: {key}')
    date.fromisoformat(spec['date'])
    if spec['fit'] not in ('Good', 'Stretch'):
        raise ValueError('Only approved Good/Stretch applications may be packaged.')
    if not spec.get('fit_approved'):
        raise ValueError('Record actual Gate 1 approval.')
    if not spec.get('fit_rationale') or len(spec.get('responsibilities', [])) != 3:
        raise ValueError('Save the fit rationale and three responsibility-to-evidence mappings.')
    # Spec paths are workspace-relative, regardless of the shell's current directory.
    spec = dict(spec, jd_file=str(resolve(ws, spec['jd_file'])), attachments=[
        dict(item, path=str(resolve(ws, item['path'])), review_file=str(resolve(ws, item['review_file'])))
        for item in spec['attachments']])
    attachments = spec['attachments']
    if not any(item.get('kind') == 'resume' for item in attachments):
        raise ValueError('A final resume is required.')
    for item in attachments:
        _check_attachment(item, ws)
    if not Path(spec['jd_file']).is_file():
        raise ValueError('Save the full JD text before packaging.')
    destination = Path(output_root) / f"{spec['date']}_{safe(spec['company'])}_{safe(spec['requisition_id'])}"
    if destination.exists():
        raise ValueError('Package already exists; do not overwrite submitted or reviewed files. Use a distinct requisition/revision.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.preparing-', dir=destination.parent))
    try:
        files = []

        def copy(source, name):
            shutil.copy2(source, temp / name)
            files.append({'archive_name': name, 'sha256': file_digest(temp / name)})

        copy(spec['jd_file'], 'job_description' + Path(spec['jd_file']).suffix)
        for n, item in enumerate(attachments, 1):
            copy(item['path'], f"{n:02d}_{safe(item['kind'])}{Path(item['path']).suffix}")
            copy(item['review_file'], f'{n:02d}_review.json')
        manifest = {k: v for k, v in spec.items() if k not in ('jd_file', 'attachments')}
        manifest.update({'schema_version': 2, 'state': 'prepared-not-submitted', 'files': files})
        (temp / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        temp.rename(destination)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--workspace')
    parser.add_argument('--spec')
    parser.add_argument('--verify')
    parser.add_argument('--out-dir')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    announce(load_config_or_empty(ws))
    try:
        if args.verify:
            print(json.dumps(verify_package(args.verify), indent=2))
        elif args.spec:
            print(prepare(read_json(resolve(ws, args.spec)), args.out_dir or ws / 'application_packages', ws))
        else:
            parser.error('Use --spec or --verify.')
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit(str(exc))


if __name__ == '__main__':
    main()
