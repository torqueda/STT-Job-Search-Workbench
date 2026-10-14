#!/usr/bin/env python3
"""answer_check.py: storytelling check for suggested answers, letter paragraphs and emails.

Run it on every suggested screening answer before the facts review (prompts/09_storytelling_check.md).
It reads answers out of a markdown file (blockquoted lines, or paragraphs of 40+ words when there are no
blockquotes), runs the known-error checks and the storytelling check on each, and exits non-zero when anything
is flagged. A flag is a prompt to fix the answer or to record a specific reason in the review. A clean run
does not mean the answer is well told.

Usage:
    python3 scripts/answer_check.py workspace/cover_letters/2026-01-05/screening_answers.md
    python3 scripts/answer_check.py --text "I built ..."
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workflow_quality import content_issues, read_document, storytelling_issues, text_digest  # noqa: E402
from workspace import announce, load_config_or_empty, workspace_dir  # noqa: E402


def extract_answers(raw):
    """Blockquoted answers; otherwise body paragraphs of 40+ words (headings, bullets and tables skipped)."""
    quoted, current = [], []
    for line in raw.splitlines():
        if line.startswith('>'):
            current.append(line[1:].strip())
        elif current:
            quoted.append(' '.join(x for x in current if x))
            current = []
    if current:
        quoted.append(' '.join(x for x in current if x))
    if quoted:
        return [q for q in quoted if q]
    paragraphs = []
    for block in re.split(r'\n\s*\n', raw):
        block = block.strip()
        if not block or block[0] in '#-*|`' or re.match(r'\d+\.', block):
            continue
        if len(block.split()) >= 40:
            paragraphs.append(' '.join(block.split()))
    return paragraphs


def check_answers(answers, ws=None):
    report = []
    for number, answer in enumerate(answers, 1):
        errors, warnings = content_issues(answer, ws)
        story = storytelling_issues(answer, ws)
        report.append({'answer': number, 'words': len(answer.split()), 'starts': answer[:70],
                       'text_sha256': text_digest(answer), 'errors': errors,
                       'editorial_checks': warnings, 'storytelling': story})
    return report


def is_flagged(item):
    return bool(item['errors'] or item['editorial_checks'] or item['storytelling'])


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('file', nargs='?', help='Markdown, text or docx file holding the suggested answers.')
    parser.add_argument('--text', help='Check one answer passed on the command line.')
    parser.add_argument('--json', action='store_true', help='Machine-readable output.')
    parser.add_argument('--workspace')
    args = parser.parse_args()
    if not args.file and not args.text:
        parser.error('give a file or --text')
    ws = workspace_dir(args.workspace)
    announce(load_config_or_empty(ws))
    answers = [args.text] if args.text else extract_answers(read_document(args.file))
    if not answers:
        sys.exit('No answers found (blockquote each answer with "> ", or write paragraphs of 40+ words).')
    report = check_answers(answers, ws)
    flagged = sum(is_flagged(r) for r in report)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for r in report:
            print(f"Answer {r['answer']} ({r['words']} words, \"{r['starts']}...\"): {'FLAGGED' if is_flagged(r) else 'clean'}")
            for label, items in (('ERROR', r['errors']), ('editorial', r['editorial_checks']), ('storytelling', r['storytelling'])):
                for item in items:
                    print(f'  [{label}] {item}')
        print(f'\n{flagged} of {len(report)} answer(s) flagged. Resolve each flag or record a specific reason in the review.')
    raise SystemExit(1 if flagged else 0)


if __name__ == '__main__':
    main()
