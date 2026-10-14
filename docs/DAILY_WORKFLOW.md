# The daily workflow

Three human checkpoints organize the work. The assistant prepares materials, scripts perform checks, and you
confirm facts and unresolved questions throughout. Each stage has a prompt in `prompts/`; the assistant is told
which one to use by `AGENTS.md`, and you can also paste the prompt yourself.

| # | Stage | Who | Output | You decide |
|---|---|---|---|---|
| 0 | Start the session | assistant | five-line status: pending, deadlines, open questions | what to do today |
| 1 | Source | assistant | grouped list of verified postings with saved full text | **Checkpoint A:** is this list satisfactory? |
| 2 | Triage | assistant | every role Good / Stretch / Poor, with why; eligibility separate from fit | **Gate 1:** which roles advance; change any fit |
| 3 | Tailor and draft | assistant | resumes by persona; grouped list with live links; drafted answers; letters when required or requested | - |
| 4 | Review | assistant | facts, role match, voice, proofreading; storytelling check | - |
| 5 | Check and apply | **you** | corrections to resumes and answers; every application submitted by hand | **Gate 2:** what is sent |
| 6 | Log | assistant | tracker rows for what you submitted; skip-list entries for what you skipped | - |
| 7 | End the session | assistant | files updated; `HANDOFF.md` entry | - |
| weekly | Review | assistant | cohort report, what is working and not | rule changes |

## 1. Source (Checkpoint A)
The assistant reads open sources first (a public listings feed, your employers' own boards, links you paste), verifies each
posting on the employer's own site, saves the full text and drops duplicates, excluded companies and out-of-scope roles. It
stops and shows you the list. Nothing is triaged until you say go. ([04_sourcing.md](../prompts/04_sourcing.md),
[SOURCING.md](SOURCING.md))

## 2. Triage (Gate 1)
For each posting: real and open? duplicate or over the company limit? **eligible** (quoted posting language against your
rules; unknown is never eligible)? and, separately, **fit**: the three central responsibilities mapped to direct, adjacent,
coursework-only or missing evidence. The verdict is **Good**, **Stretch** (skill or level, with the specific gap) or **Poor**,
with a reason. The recommended set keeps stretches near your share (default 30%), skill stretches before level stretches.
You change any verdict you disagree with and say go. ([05_triage.md](../prompts/05_triage.md))

## 3. Tailor and draft
A persona per role by core function; a batch spec that only selects and orders; generated DOCX. The assistant reports the
**final list grouped by persona/resume (fewest roles first), each role with its live posting link**, required materials and
deadlines. If it can see application questions it drafts answers from your ledger, including confirmed facts and motives recorded from earlier answers; you bring any
later-discovered questions one at a time or in a batch. Cover letters are optional by default; the assistant says when one is
required. ([06_tailoring.md](../prompts/06_tailoring.md), [07_letters_and_answers.md](../prompts/07_letters_and_answers.md))

## 4. Review
Facts first (claim IDs, ownership, scope), then role match and voice, then proofreading, plus the storytelling check on every
answer. A review is recorded and bound to normalized extracted text. ([08_review.md](../prompts/08_review.md),
[09_storytelling_check.md](../prompts/09_storytelling_check.md))

## 5. You check and apply (Gate 2)
Open each document and answer. Correct anything: those corrections are valuable, and the assistant learns from them (see
[PERSONALIZING.md](PERSONALIZING.md)). Finalize resumes your way ([RESUME_HANDLING.md](RESUME_HANDLING.md)). Complete every
application yourself and submit each part by hand.

## 6. Log
When everything is submitted or skipped, tell the assistant. It logs submitted applications with the date you give (dry-run
first, so you see the row), records skipped ones in the skip list, and updates the tracker you chose.
([10_logging_and_weekly_review.md](../prompts/10_logging_and_weekly_review.md))

## 7. End the session
The assistant updates the files that changed (a rule you stated, a fact you added, an exclusion) and writes a `HANDOFF.md`
entry, so tomorrow's session starts where this one stopped. ([11_session_handoff.md](../prompts/11_session_handoff.md))

## A day in commands (what the assistant runs for you)

```bash
python3 scripts/doctor.py                                        # workspace consistent?
python3 scripts/sourcing.py --role-profile data --source github --hours 24
python3 scripts/employer_watch.py --days 2
python3 scripts/check_company.py "Acme" --url https://... --requisition-id 123
python3 scripts/skip_list.py add --url https://... --reason "requires 6+ years" --company Acme
python3 scripts/resume_generator.py --spec resume_versions/2026-01-06.json --dry-run
python3 scripts/answer_check.py cover_letters/2026-01-06/screening_answers.md
python3 scripts/tracker_update.py --title ... --company ... --link ... --date 2026-01-06 --confirmed-submitted --resume-spec resume_versions/2026-01-06.json --dry-run
```

## Cadence
Source as often as your profile says: postings fill quickly, which is why the workflow is built to get from sourcing to a sent
application in one day. Run the weekly review once a week. Everything else is on demand.
