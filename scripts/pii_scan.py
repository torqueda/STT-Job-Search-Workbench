#!/usr/bin/env python3
"""pii_scan.py: release hygiene. Scan a folder for personal information before it is published.

Two layers:

1. Built-in patterns for things that should never be in a public repository: email addresses (other than
   example/noreply domains), phone numbers, US Social Security numbers, home-directory paths, API-key-looking
   strings and LinkedIn profile URLs (other than placeholders).
2. An optional deny-list file of your own terms (your name, employers, schools, project names, numbers from
   your resume). Keep that file OUTSIDE the repository: it is itself a list of personal information.
   One term per line; lines starting with # are comments; prefix a line with "re:" for a regular expression.
   Plain terms match case-insensitively on word boundaries.

Files may be exempted from specific terms with --allow PATH:TERM (for example the author's name in LICENSE).

Exit status is 1 when anything is found. A clean scan is evidence, not proof: still read the diff before you push.

Usage:
    python3 scripts/pii_scan.py --root . --denylist ~/private/denylist.txt --allow LICENSE:Jane
"""
import argparse
import re
import sys
from pathlib import Path

SKIP_DIRS = {'.git', '__pycache__', '.venv', 'node_modules'}
PRIVATE_ROOT_DIRS = {'workspace'}  # the user's own workspace at the repository root; never published
EMAIL_OK = re.compile(r'@(?:[\w.-]*\.)?(?:example\.(?:com|org|net)|users\.noreply\.github\.com|noreply\.[\w.]+)$', re.I)
PATTERNS = {
    'email': re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}'),
    'phone': re.compile(r'(?<![\w.])(?:\+?1[\s.-]?)?\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b'),
    'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    'home path': re.compile(r'(?:/Users/|/home/)(?!you\b|name\b|username\b|<)[A-Za-z0-9._-]+|C:\\Users\\[A-Za-z0-9._-]+'),
    'api key': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})\b'),
    'linkedin profile': re.compile(r'linkedin\.com/in/(?!your-|jordan-example|username|handle)[A-Za-z0-9_-]+', re.I),
}


def is_placeholder_phone(text):
    """All-zero placeholders and the reserved fictional range 555-0100 to 555-0199 are not personal data."""
    digits = re.sub(r'\D', '', text)
    all_zero = set(digits) == {'0'}
    reserved_fictional = digits[-7:-4] == '555' and digits[-4:-2] == '01'
    return all_zero or reserved_fictional


def load_denylist(path):
    terms = []
    for line in Path(path).expanduser().read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        terms.append((line, re.compile(line[3:], re.I) if line.startswith('re:') else re.compile(r'(?<!\w)' + re.escape(line) + r'(?!\w)', re.I)))
    return terms


def iter_files(root):
    for path in sorted(Path(root).rglob('*')):
        parts = path.relative_to(root).parts
        if path.is_file() and not any(part in SKIP_DIRS for part in parts) and parts[0] not in PRIVATE_ROOT_DIRS:
            yield path


def scan_text(text, deny, allowed_terms=()):
    """Return [(line_number, kind, matched_text)]."""
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                if kind == 'email' and EMAIL_OK.search(match.group(0)):
                    continue
                if kind == 'phone' and is_placeholder_phone(match.group(0)):
                    continue
                hits.append((number, kind, match.group(0)))
        for term, pattern in deny:
            if term in allowed_terms:
                continue
            for match in pattern.finditer(line):
                hits.append((number, f'deny-list: {term}', match.group(0)))
    return hits


def scan(root, denylist=None, allow=None):
    root = Path(root).resolve()
    deny = load_denylist(denylist) if denylist else []
    allow = allow or {}
    findings = []
    for path in iter_files(root):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            findings.append((relative, 0, 'symlink', 'not scanned: inspect target before publishing'))
            continue
        # Personal data can appear in filenames as well as file contents.
        for _, kind, matched in scan_text(relative, deny, allow.get(relative, ())):
            findings.append((relative, 0, kind, 'in file name: ' + matched))
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            findings.append((relative, 0, 'binary file', 'not scanned: inspect by hand or remove'))
            continue
        if '\x00' in text:
            findings.append((relative, 0, 'binary file', 'not scanned: inspect by hand or remove'))
            continue
        for number, kind, matched in scan_text(text, deny, allow.get(relative, ())):
            findings.append((relative, number, kind, matched))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--root', default='.')
    parser.add_argument('--denylist', help='A file of personal terms to look for (keep it outside the repository).')
    parser.add_argument('--allow', action='append', default=[], metavar='PATH:TERM',
                        help='Exempt a deny-list term in one file, for example LICENSE:Jane.')
    args = parser.parse_args()
    allow = {}
    for item in args.allow:
        path, _, term = item.partition(':')
        allow.setdefault(path, set()).add(term)
    findings = scan(args.root, args.denylist, allow)
    for relative, number, kind, matched in findings:
        print(f'{relative}:{number}  [{kind}]  {matched}')
    print(f'\n{len(findings)} finding(s) in {Path(args.root).resolve()}')
    sys.exit(1 if findings else 0)


if __name__ == '__main__':
    main()
