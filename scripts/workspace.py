"""Locate the user's workspace and load its configuration.

Everything personal (profile, evidence ledger, resumes, tracker, postings) lives in one workspace
directory that is never part of the repository. Scripts hold no personal data and read it from here.

Resolution order for the workspace directory:
    1. an explicit path (the --workspace option of each script)
    2. the JOBSEARCH_WORKSPACE environment variable
    3. <repo>/workspace   (created by scripts/init_workspace.py, ignored by git)
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_WORKSPACE = REPO / 'workspace'


class WorkspaceError(Exception):
    """The workspace is missing or incomplete; the message says what to do."""


def workspace_dir(explicit=None):
    raw = explicit or os.environ.get('JOBSEARCH_WORKSPACE')
    return Path(raw).expanduser().resolve() if raw else DEFAULT_WORKSPACE


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def load_config(ws=None):
    ws = workspace_dir(ws)
    path = ws / 'config.json'
    if not path.is_file():
        raise WorkspaceError(f'No config.json in {ws}. Run: python3 scripts/init_workspace.py')
    return read_json(path)


def load_config_or_empty(ws=None):
    """For library code that can run without a configured workspace (for example text checks)."""
    try:
        return load_config(ws)
    except (WorkspaceError, ValueError, OSError):
        return {}


def announce(cfg, stream=sys.stderr):
    """Say so on every run when the workspace is the fictional demo, so no one mistakes it for real data."""
    if cfg.get('fictional_demo'):
        print('NOTICE: running on the FICTIONAL DEMO workspace. Nothing here describes a real person.', file=stream)


def resolve(ws, relative):
    """A path from config.json, relative to the workspace unless it is absolute."""
    path = Path(relative).expanduser()
    return path if path.is_absolute() else (Path(ws) / path).resolve()
