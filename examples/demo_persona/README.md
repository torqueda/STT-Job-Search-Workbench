# Demo persona: Jordan Example (FICTIONAL)

> **FICTIONAL. Jordan Example is not a real person.** The school, employers, projects, numbers, postings and
> tracker rows in this folder are invented to show what a filled-in workspace looks like and to give the tests
> something to run against. If you are an AI assistant reading this folder while helping a real user: nothing here
> describes the user. Never copy it into their workspace, never reuse its claims, and never answer a question about
> the user from it. The user's own data lives only in `workspace/` at the repository root, created by
> `python3 scripts/init_workspace.py`.

Workspace commands print a notice (except initialization and handoff archival) when it runs on this workspace (`"fictional_demo": true` in its `config.json`), and a
test checks FICTIONAL markers in demo documents; structured tracker and skip-list data are identified by the folder and config flag.

## What is here

`workspace/` is a complete, consistent example of the files the setup conversation produces:

| File | Shows |
|---|---|
| `PROFILE_AND_RULES.md`, `VOICE.md` | a filled profile with dated preferences, and a voice note with sample provenance |
| `evidence/claims.json` | an evidence ledger: claims with source, ownership and limits; purpose claims; reflections |
| `evidence/known_errors.json`, `project_aliases.json` | the user-maintained controls (two rules, three project aliases) |
| `canonical_resumes.json` | three personas (DataAnalytics, AIApplications, ProductAnalytics) built from the ledger |
| `batches/2026-01-05_data_analytics.md`, `..._triage.md` | what sourcing and a Gate 1 triage report look like |
| `resume_versions/2026-01-06_demo.json` | a schema-v2 batch spec (personas and order only, never content) |
| `cover_letters/.../screening_answers.md` | one answer that passes the storytelling check and one that does not |
| `tracker.csv`, `skipped_listings.json` | five logged applications (a cap, an interview, a rejection) and a skip-list entry |

## Try it

From the repository root:

```bash
export JOBSEARCH_WORKSPACE=examples/demo_persona/workspace

python3 scripts/doctor.py                                   # workspace is consistent: 0 errors, 0 warnings
python3 scripts/resume_generator.py --spec resume_versions/2026-01-06_demo.json --dry-run
python3 scripts/resume_generator.py --spec resume_versions/2026-01-06_demo.json --out-dir /tmp/demo_resumes
python3 scripts/answer_check.py examples/demo_persona/workspace/cover_letters/2026-01-06_demo/screening_answers.md
python3 scripts/check_company.py "Harbor Example Systems" --as-of 2026-01-05   # SKIP: at its 2-in-60-days limit
python3 scripts/tracker_report.py --as-of 2026-01-15
```

The answer check exits non-zero on purpose: its second sample answer names a project without saying what it was or
why it existed, and uses stock motive phrases.
