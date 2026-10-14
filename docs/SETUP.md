# Setup in detail

## What you need
- Python 3.10 or newer. `python3 -m pip install -r requirements.txt` installs the optional pieces
  (`python-docx` for DOCX output, `openpyxl` for an Excel tracker, `pypdf` to read PDFs). The core scripts use only the
  standard library.
- An AI assistant that can read and write files in a folder (ideal), or one that can at least accept attached files
  ([LLM_COMPATIBILITY.md](LLM_COMPATIBILITY.md)).
- Your current resume in any format.

## Steps
1. `git clone` this repository (or download it) and `cd` into it.
2. `python3 scripts/init_workspace.py` creates `workspace/` from `templates/`. It never overwrites existing files, so it is safe
   to run again after pulling an update. `workspace/` is ignored by git.
   - Prefer another location? `--workspace ~/Documents/my-job-search` (or set `JOBSEARCH_WORKSPACE`) and use the same option
     for the other scripts.
   - Want it versioned or backed up? Use a **private** repository or a synced folder. Never publish it.
3. Open your assistant in the repository folder and say: *Read AGENTS.md, then run the initial setup from
   prompts/01_setup_interview.md.*
4. Follow the interview. It covers, in order: material to collect (resume, experience, writing samples), profile and rules
   (the musts and must-nots), your voice, then evidence and personas in the next sessions.
5. `python3 scripts/doctor.py` checks that the files agree.

## Before the first session (optional, saves time)
- Gather: resume, LinkedIn export or portfolio links, course and project lists, anything you wrote for an application.
- Decide roughly: the two or three job families you want, cities or regions, companies or industries you will not apply to,
  your salary floor, how many applications a week is realistic, how you want to track them.
- Think about your work-authorization situation in exact terms (status, dates, whether you will need sponsorship now or later).

## What setup produces
| File | From |
|---|---|
| `PROFILE_AND_RULES.md`, `config.json` | the setup interview |
| `VOICE.md` | your writing samples and stated preferences |
| `evidence/claims.json`, `BOUNDARIES.md`, `project_aliases.json` | the evidence interview (`prompts/02_evidence_builder.md`) |
| `canonical_resumes.json`, `base_resume.json` | personas (`prompts/03_personas_and_resumes.md`) |
| `tracker.csv` | empty CSV copied during initialization (or point `config.json` at your Excel file) |

You do not need a perfect result. Expect to add rules, aliases and known errors in the first weeks
([PERSONALIZING.md](PERSONALIZING.md)).

## Using an existing spreadsheet as the tracker
Set `config.json` -> `tracker` to `{"format": "xlsx", "path": "...", "sheet": "...", "header_row": N, "columns": {...}}` with the
column letter for each field (see [TRACKING.md](TRACKING.md)). Missing headers are added; your other cells and sheets are left
alone, and the file is backed up before each write. Close it in Excel before the assistant writes.

## Troubleshooting
| Symptom | Likely cause |
|---|---|
| `No config.json in ...` | run `init_workspace.py`, or pass `--workspace` / set `JOBSEARCH_WORKSPACE` |
| `Refusing to overwrite existing resumes` | choose a new version label or a new output folder; existing drafts are preserved |
| `Record the actual submission date` | supply the user-confirmed date with `--date YYYY-MM-DD` |
| `Stale canonical revision` | a persona changed after the spec was written: re-read the persona and update the spec's `canonical_revision` |
| `Legacy spec rejected` | the spec lacks `"schema_version": 2` |
| `GATE 1 not passed` | the spec has `"approved": false`; set it to true only after you chose the roles |
| `Another tracker writer is active` | a `.writer-lock` file is left over from a crashed run; check nothing is running, then delete it |
| `Close the workbook in Excel` | Excel has the file open |
| `python-docx is not installed` | `python3 -m pip install python-docx` |
