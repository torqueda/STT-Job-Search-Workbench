#!/usr/bin/env python3
"""cover_letter_generator.py: render reviewed cover letters for approved applications.

A letter is a schema_version 2 spec entry with the company, target job, requisition, date, body paragraphs and
a review object tied to the SHA-256 of the exact body text (see prompts/08_review.md). Known factual errors
block generation; style warnings need a recorded resolution. Mechanical checks cannot establish truth or a
human voice, so read the rendered letter yourself.

Usage:
    python3 scripts/cover_letter_generator.py --spec cover_letter_versions/2026-01-05.json --review-digests
    python3 scripts/cover_letter_generator.py --spec cover_letter_versions/2026-01-05.json --dry-run
    python3 scripts/cover_letter_generator.py --spec cover_letter_versions/2026-01-05.json

--review-digests prints each body's hash and checks (it does not review or approve anything). Generation
requires "approved": true. Files are written under a batch folder and never overwrite an existing letter.
A letter with "general": true is an undated, unaddressed supporting letter for quick-apply roles.

Letters are optional by default (see PROFILE_AND_RULES.md); the assistant says when a posting requires one.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_generator import clean_filename_part, output_filename  # noqa: E402
from workflow_quality import content_issues, require_v2, storytelling_issues, text_digest, validate_review  # noqa: E402
from workspace import announce, load_config_or_empty, read_json, workspace_dir  # noqa: E402

DEFAULT_RULES = {
    'min_words': 120,
    'max_words': 350,
    # Optional fixed sentences; leave null to not enforce any particular opening or closing.
    'required_opening': None,   # e.g. "I am writing to express my interest in the {job} position at {company}."
    'required_closing': None,   # e.g. "Thank you for your consideration."
    'banned_phrases': [
        'i am uniquely qualified', 'i would be an invaluable asset', 'i am confident that my skills align perfectly',
        'i am thrilled to submit my application', 'at the intersection of', 'leverage my skill set',
        'fast-paced environment', 'hit the ground running', 'passionate about innovation',
    ],
}


def letter_rules(cfg):
    return {**DEFAULT_RULES, **(cfg.get('letters') or {})}


def word_count(paragraphs):
    return len(re.findall(r"[A-Za-z0-9'-]+", ' '.join(paragraphs)))


def parse_contact(contact_line):
    """Email, phone and LinkedIn from base_resume.json's pipe-separated contact line, so this script keeps no copy."""
    parts = [p.strip() for p in contact_line.split('|')]
    email = next((p for p in parts if '@' in p), '')
    phone = next((p for p in parts if re.search(r'\d{3}.*\d{3}.*\d{4}', p)), '')
    linkedin = next((p for p in parts if 'linkedin.com' in p.casefold()), '')
    return email, phone, linkedin


def validate_letter(letter, index, rules):
    """Human-readable warnings for one letter. Never fatal."""
    general = bool(letter.get('general'))
    label = letter.get('company') or ('General' if general else f'#{index + 1}')
    body = letter.get('body_paragraphs') or []
    if not body:
        return [f'[{label}] no body_paragraphs; nothing to render.']
    warns = []
    words = word_count(body)
    if not rules['min_words'] <= words <= rules['max_words']:
        warns.append(f'[{label}] body is {words} words; check completeness and the employer limit. Never pad to reach a target.')
    text = ' '.join(body).casefold()
    warns += [f'[{label}] contains a banned phrase: "{p}".' for p in rules['banned_phrases'] if p in text]
    opening = rules.get('required_opening')
    if opening and not general:
        expected = opening.format(job=letter.get('target_job', '[JOB]'), company=letter.get('company', '[COMPANY]'))
        if not body[0].strip().startswith(expected):
            warns.append(f'[{label}] does not open with the configured sentence: "{expected}"')
    closing = rules.get('required_closing')
    if closing and not body[-1].strip().endswith(closing):
        warns.append(f'[{label}] does not close with the configured sentence: "{closing}"')
    return warns


def _docx_imports():
    try:
        from docx import Document
        from docx.shared import Inches, Pt
        return Document, Pt, Inches
    except ImportError:
        sys.exit('python-docx is not installed. Run: python3 -m pip install python-docx')


def build_document(base, letter):
    Document, Pt, Inches = _docx_imports()
    email, phone, linkedin = parse_contact(base['contact_line'])
    doc = Document()
    for section in doc.sections:
        section.top_margin = section.bottom_margin = Inches(0.8)
        section.left_margin = section.right_margin = Inches(0.9)
    normal = doc.styles['Normal']
    normal.font.name, normal.font.size = 'Calibri', Pt(11)

    def para(text='', bold=False, after=8):
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(after)
        paragraph.paragraph_format.line_spacing = 1.15
        if text:
            run = paragraph.add_run(text)
            run.bold, run.font.name = bold, 'Calibri'

    para(base['name'], bold=True, after=0)
    if email or phone:
        para(' | '.join(b for b in (email, phone) if b), after=0)
    para(linkedin, after=16) if linkedin else para(after=16)
    if not letter.get('general'):
        para(letter.get('date') or datetime.date.today().strftime('%B %d, %Y'), after=16)
    para('Dear Hiring Manager,', after=12)
    for paragraph in letter.get('body_paragraphs', []):
        para(paragraph.strip(), after=12)
    para('Kind regards,', after=24)
    para(base['name'])
    return doc


def main():
    parser = argparse.ArgumentParser(description='Generate one .docx cover letter per approved, reviewed letter.')
    parser.add_argument('--spec', required=True)
    parser.add_argument('--workspace')
    parser.add_argument('--base')
    parser.add_argument('--out-dir')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--review-digests', action='store_true', help='Print body digests and checks; does not approve drafts.')
    args = parser.parse_args()

    ws = workspace_dir(args.workspace)
    cfg = load_config_or_empty(ws)
    announce(cfg)
    rules = letter_rules(cfg)
    base = read_json(args.base or ws / 'base_resume.json')
    spec_path = Path(args.spec) if Path(args.spec).is_absolute() or Path(args.spec).exists() else ws / args.spec
    spec = read_json(spec_path)
    letters = spec.get('letters', [])
    if not letters:
        sys.exit("Spec contains no 'letters'.")
    if args.list:
        print(f"Spec: {spec_path.name}  |  approved={spec.get('approved', False)}  |  {len(letters)} letter(s)")
        for i, letter in enumerate(letters, 1):
            print(f"  {i}. {letter.get('company', '?')}  ->  {letter.get('target_job', '(no job listed)')}")
        return
    try:
        require_v2(spec)
    except ValueError as exc:
        sys.exit(str(exc))
    if args.review_digests:
        for letter in letters:
            text = '\n'.join(letter.get('body_paragraphs', []))
            errors, warnings = content_issues(text, ws)
            print(json.dumps({'company': letter.get('company'), 'text_sha256': text_digest(text), 'errors': errors,
                              'editorial_checks': warnings + storytelling_issues(text, ws)}, indent=2))
        return
    problems = []
    for letter in letters:
        text = '\n'.join(letter.get('body_paragraphs', []))
        found, _ = validate_review(text, letter.get('review'), require_company=not letter.get('general'), writing=True, ws=ws)
        problems += [f"[{letter.get('company', '?')}] {e}" for e in found]
        for key in (() if letter.get('general') else ('target_job', 'requisition_id', 'date')):
            if not letter.get(key):
                problems.append(f'Missing {key}; give an explicit unavailable-ID explanation if the employer has no requisition.')
    if problems:
        sys.exit('Review required before generation:\n' + '\n'.join(problems))
    if not spec.get('approved', False):
        sys.exit('GATE 1 not passed: the spec has "approved": false (or missing). No letter is written until you have '
                 'approved the triage buckets. (--dry-run previews validation.)')
    warnings = [w for i, letter in enumerate(letters) for w in validate_letter(letter, i, rules)]
    if warnings:
        print('Content warnings:')
        for w in warnings:
            print('  ! ' + w)
        print()
    if any(not l.get('company') and not l.get('general') for l in letters):
        sys.exit('Every letter needs a "company" so its output file can be named.')

    out_dir = (Path(args.out_dir) if args.out_dir else ws / 'cover_letters') / clean_filename_part(spec['batch'], 'batch')

    def name_for(letter):
        if letter.get('general') and not letter.get('company'):
            return output_filename(base, 'Cover Letter', 'General')
        return output_filename(base, 'Cover Letter', letter['company'])

    names = [name_for(l) for l in letters]
    if len(names) != len(set(names)):
        sys.exit('Two letters in this batch would write the same file. One letter per company per batch, or split the batch.')
    existing = [n for n in names if (out_dir / n).exists()]
    if existing:
        sys.exit('Existing letters preserved. Use a new revision in the batch name: ' + ', '.join(existing))
    if args.dry_run:
        print('[DRY RUN] Reviewed outputs: ' + ', '.join(str(out_dir / n) for n in names))
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    for letter, name in zip(letters, names):
        build_document(base, letter).save(out_dir / name)
        print(f'Generated {name}  ->  {out_dir / name}')
    print(f'\nDone. {len(names)} cover letter file(s) in {out_dir}.')
    print('Next: review each file, export to PDF yourself, then submit (Gate 2).')


if __name__ == '__main__':
    main()
