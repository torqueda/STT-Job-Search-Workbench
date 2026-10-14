# Scripts

Plain Python. Standard library only, except `python-docx` (DOCX), `openpyxl` (Excel tracker) and `pypdf` (reading PDFs). Workspace
commands take `--workspace PATH` (default `JOBSEARCH_WORKSPACE`, then `./workspace`) and announce the fictional demo workspace when they
run on it (except initialization and handoff archival). `pii_scan.py` takes `--root` instead. None submits anything, logs in or sends a message.

| Script | What it does | Typical use |
|---|---|---|
| `init_workspace.py` | Creates the workspace from `templates/`; never overwrites | `python3 scripts/init_workspace.py` |
| `doctor.py` | Validates the workspace: required files, ledger fields, persona references, required claims, regexes, base-resume lines vs ledger, tracker | after any edit |
| `workflow_quality.py` | Library: evidence resolution, known-error and editorial checks, storytelling check, review binding. CLI prints a file's digest and checks | `python3 scripts/workflow_quality.py final.docx --writing` |
| `answer_check.py` | Storytelling check on answers in a markdown file (blockquotes, or paragraphs of 40+ words) | `python3 scripts/answer_check.py answers.md` |
| `resume_generator.py` | One DOCX per persona version; needs `approved: true`; refuses unsupported experience bullets and existing outputs | `--spec <spec> --dry-run` |
| `cover_letter_generator.py` | DOCX letters from reviewed specs; `--review-digests` prints hashes | `--spec <spec> --review-digests` |
| `application_package.py` | Freezes the exact final files with hashes; `--verify` re-checks | `--spec specs/package.json` (spec and attachment paths relative to the workspace) |
| `sourcing.py` | Builds a dated batch from a public feed, a file or pasted text; applies filters, tracker and skip list | `--role-profile data --source github --hours 24` |
| `employer_watch.py` | Reads employers' Greenhouse/Lever boards for recent postings in your metros | `--days 2` |
| `check_company.py` | Duplicate, requisition, company-limit and exclusion check | `"Acme" --url ... --requisition-id ...` |
| `skip_list.py` | Append-only log of roles rejected at Gate 1 | `add --url ... --reason ...` / `list` |
| `tracker_update.py` | Logs a submitted application or updates a stage; backup, lock, atomic write, event log | `... --confirmed-submitted --dry-run` |
| `tracker_report.py` | Cohort report for the weekly review | `--minimum-age-days 30` |
| `archive_handoff.py` | Moves older handoff entries to `history/` | `--keep 10` |
| `pii_scan.py` | Scans a folder for personal data before publishing | `--root . --denylist ~/private/terms.txt` |
| `tracker.py`, `workspace.py` | Libraries: tracker backends (CSV, Excel); workspace and config resolution | - |

## Exit codes
`0` success or clean; `1` a check failed or something was flagged (`doctor.py`, `answer_check.py`, `check_company.py`,
`pii_scan.py`, `workflow_quality.py` when errors exist); other failures exit with a message on stderr.
