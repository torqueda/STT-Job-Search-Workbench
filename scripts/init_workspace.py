#!/usr/bin/env python3
"""init_workspace.py: create your personal workspace from the blank templates.

Copies templates/ into a workspace folder (default: ./workspace, which git ignores) and creates the empty
working folders. Existing files are never overwritten, so it is safe to run again after pulling an update.

Your workspace holds everything personal: profile, evidence ledger, resumes, postings, tracker. Keep it out of
any public repository. If you want it versioned or backed up, use a private repository or a synced folder.

Usage:
    python3 scripts/init_workspace.py [--workspace PATH]
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace import REPO, workspace_dir  # noqa: E402

WORKING_FOLDERS = ['batches', 'job_descriptions', 'resume_versions', 'tailored_resumes', 'cover_letters',
                   'cover_letter_versions', 'reviews', 'application_packages', 'backups', 'interview_prep']


def init(ws, templates=None):
    """Copy each template that does not exist yet. Returns (created, kept)."""
    templates = Path(templates or REPO / 'templates')
    created, kept = [], []
    for source in sorted(p for p in templates.rglob('*') if p.is_file() and not p.name.startswith('.')):
        relative = source.relative_to(templates)
        target = Path(ws) / relative
        if target.exists():
            kept.append(str(relative))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        created.append(str(relative))
    for folder in WORKING_FOLDERS:
        (Path(ws) / folder).mkdir(parents=True, exist_ok=True)
    return created, kept


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--workspace')
    args = parser.parse_args()
    ws = workspace_dir(args.workspace)
    created, kept = init(ws)
    print(f'Workspace: {ws}')
    print(f'  created {len(created)} file(s), kept {len(kept)} existing file(s)')
    print('\nNext steps:')
    print('  1. Open your AI assistant in this repository folder (so it can read and write files).')
    print('  2. Tell it: "Read AGENTS.md, then start the initial setup from prompts/01_setup_interview.md."')
    print('  3. When setup is done, run: python3 scripts/doctor.py')


if __name__ == '__main__':
    main()
