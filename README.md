# Source-Triage-Tailor Job Search Workbench

**STT Job Search Workbench** is a file-based workflow for sourcing, evaluating, preparing and tracking job applications
with an AI assistant.
The assistant drafts from an evidence ledger. You choose the roles, review the final materials and submit each
application yourself.

The project addresses two practical problems with which I became familiar through personal use: AI drafts can overstate
or invent experience, and they can fail to capture the relevant and important information which can be found within a
person's work and projects. This is why it's so important for a user to verify every material which is submitted to a
potential employer.

## How it started

I built this piece by piece during my daily job search, then made it a project of its own for my portfolio. Postings
advertising automatic application agents prompted me to think about who verifies the files and answers sent to employers,
and how a workflow could be tailored to each applicant's own experience and preferences.

I (Tomas Orqueda) built this with Claude, through Claude Code, and Claude is the only assistant I have ever run it with.
The prompts are plain Markdown and the scripts are plain Python, so the design can be used with other file-capable
assistants. Their behavior in a job-search session has not been evaluated; see [assistant compatibility](docs/LLM_COMPATIBILITY.md).

## What it did for me

This workflow has made it easier for me to find roles that fit my experience level and interests, and it has made resume
tailoring and answer drafting much smoother. That is the only claim I make for it.

## Why it is built this way

The controls grew out of problems encountered in real use. These anonymized examples explain some of the design choices:

- On one occasion a drafted resume line claimed more than the evidence supported: a modeled estimate was worded as a
  realized saving. Resume claims now live in an evidence ledger with their source, ownership and limits.
- On one occasion a link supplied for one role opened a different posting at the same employer. The workflow now verifies
  the title, link, team and requisition together on the employer's own page.
- Early batch specs carried their own copy of resume content, so an older batch could bring back superseded wording.
  Batch specs now select a persona and reorder its projects; stale persona revisions are rejected.
- A drafted answer named a project the reader had never heard of and jumped to tools and numbers. A separate storytelling
  check now asks what the project was and why it existed, using only recorded evidence.

The [design decisions](docs/DESIGN_DECISIONS.md) document maps these and other failures to their controls and tests.

## What is automated, and what you do

| Assistant | Python helpers | You |
|---|---|---|
| Read your rules and evidence; find and verify postings | Read public feeds and employer boards; filter leads and duplicates | Confirm the sourcing list before triage |
| Assess eligibility separately from fit; recommend roles | Check company exclusions, duplicates and planning limits | Choose which roles advance and correct any fit judgment |
| Select a resume persona; draft required answers and letters | Generate DOCX drafts; check claim references, revisions and review digests | Verify facts, wording, eligibility answers and final layout |
| Record corrections, preferences and session handoffs | Archive reviewed files; update CSV/Excel and report recorded outcomes | Submit applications and messages yourself; confirm submission and its date |

The repository contains no application-submission or login automation. Approval fields record decisions; they cannot
prove that a person made them. The assistant must follow the prompts, and you remain responsible for what you send.

## The interaction

```text
YOU: experience, goals, preferences and corrections
                     |
                     v
PRIVATE WORKSPACE: rules + evidence ledger + resume personas
                     |
                     v
LLM: source and verify postings <-- Python: public feeds, filters
                     |
YOU: confirm the sourcing list                 [Checkpoint A]
                     |
LLM: triage eligibility and fit <-- Python: duplicates, limits
                     |
YOU: choose roles to advance                           [Gate 1]
                     |
LLM: tailor, draft and review <-- Python: DOCX, evidence checks
                     |
YOU: check final files and answers; submit them yourself [Gate 2]
                     |
YOU: confirm what was submitted and when
                     |
LLM + Python: log results, preserve files, write handoff
                     |
                     +--> next session reads the updated workspace
```

A **persona** is a resume for one job family. A batch selects a persona and may reorder its projects; it cannot
replace its content. New wording goes into the evidence ledger first, with a source and a revision.

## Try it without personal data

Python 3.10 or newer is required.

```bash
git clone https://github.com/torqueda/STT-Job-Search-Workbench.git
cd STT-Job-Search-Workbench
python3 -m venv .venv
source .venv/bin/activate                 # Windows PowerShell: .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
make test
make demo
```

Without `make`, run `python3 -m unittest discover -s tests` and the commands in the
[fictional demo guide](examples/demo_persona/README.md). The demo previews generation and deliberately includes a
company at its application limit and an answer that needs rewriting. Neither represents a real applicant.

Core checks use the Python standard library. `python-docx` enables DOCX generation, `openpyxl` enables Excel tracking,
and `pypdf` enables reading an existing PDF for review. The test suite needs `python-docx` and `openpyxl`; no test uses
`pypdf`.

## Set up your own search

```bash
python3 scripts/init_workspace.py         # creates workspace/; never overwrites existing files
```

Open a file-capable assistant in this folder and say:

> Read AGENTS.md, then run the initial setup from prompts/01_setup_interview.md.

Setup collects your goals, eligibility rules, experience and writing preferences. A resume is a starting point for
questions, not evidence by itself: you confirm the claims and their scope. Then build the ledger with
[`02_evidence_builder.md`](prompts/02_evidence_builder.md) and approve job-family personas with
[`03_personas_and_resumes.md`](prompts/03_personas_and_resumes.md). Finish with `python3 scripts/doctor.py`.

For each later session, start with [`00_session_start.md`](prompts/00_session_start.md). The files carry the memory
between conversations. See [setup](docs/SETUP.md), [the daily workflow](docs/DAILY_WORKFLOW.md) and
[finalizing resumes](docs/RESUME_HANDLING.md) for the full process.

## Tailor it as you use it

Your settings belong in `workspace/`, not in the scripts or fictional examples:

- `PROFILE_AND_RULES.md`: job families, eligibility, geography, salary, cadence and decisions.
- `config.json`: filters, company limits, tracker location, employer-board filters and document limits.
- `VOICE.md`: your writing samples, their authorship and dated preferences.
- `evidence/`: sourced claims, motives in your words, factual boundaries, known errors and project aliases.
- `canonical_resumes.json`: approved job-family personas assembled from ledger claims.

Corrections become dated rules or evidence, according to your chosen confirmation policy. Changing a claim or persona
requires a `change_note` and a new revision; regenerate affected drafts and re-review changed text. This is persistent
file-based context, not model training. [Personalizing the workflow](docs/PERSONALIZING.md) explains the learning loop.

## Help test it

Testing needs no personal data: run the tests and the fictional demo, or check how your assistant behaves on the demo
workspace. The [testing guide](docs/TESTING_GUIDE.md) lists the steps, what to report and what never to paste, and the
[tester feedback form](https://github.com/torqueda/STT-Job-Search-Workbench/issues/new?template=tester-feedback.yml)
collects the results.

## Repository map

```text
AGENTS.md / CLAUDE.md     assistant instructions and entry point
prompts/                 setup and stage-by-stage interactions
scripts/                 CLI tools and shared Python modules
templates/               blank workspace files and spec examples
examples/demo_persona/   fictional workspace used by the demo and tests
tests/                   offline regression tests; no real applicant data
docs/                    setup, testing, design, evidence, sourcing, tracking and release guides
workspace/               private applicant data; created locally, ignored by Git
```

See the [script reference](docs/SCRIPTS.md), [architecture](docs/ARCHITECTURE.md),
[evidence model](docs/EVIDENCE_MODEL.md) and [design decisions](docs/DESIGN_DECISIONS.md).

## Checks and limits

- `make test` runs offline regression tests. Network responses are stubbed. GitHub Actions runs tests and a privacy scan.
- `doctor.py` checks workspace consistency. The resume generator rejects unsupported project/experience bullets and stale persona
  references. Identity fields, skills and education still require a factual review.
- Reviews bind to extracted text with whitespace normalized, plus the ledger revision. Packages hash the archived file
  bytes. Neither establishes truth or guarantees document layout.
- Public-feed and employer-board scripts return leads. The assistant verifies each retained role on the employer's site.
  No scripts scrape logged-in job boards; any assisted reading requires your request and the site's permission.
- Job-search use has been reported with Claude. Other assistants and broader user outcomes have not been evaluated.
  See [compatibility and its manual checks](docs/LLM_COMPATIBILITY.md).
- Setup and evidence maintenance take effort. There is no measured claim that this saves a particular amount of time,
  improves interview rates, or outperforms a paid service.

## Privacy and publishing

Keep resumes, contacts, trackers, postings and submitted files in your private workspace. Git ignores the default
`workspace/`, but an ignore rule does not remove previously committed files and does not protect a folder copied into a ZIP.
A local workspace may still be sent to your assistant's provider; check that provider's data settings before sharing it.

Run `make scan` before publishing. Add a private deny-list with `make scan DENYLIST=/path/to/private/terms.txt` to check
names, employers and other terms the built-in patterns cannot recognize. A clean scan is evidence, not proof, and does
not inspect Git history. Follow the [release checklist](docs/RELEASING.md).

## License

[MIT](LICENSE). Built by Tomas Orqueda with Claude; human review and submission are part of the design.
