# Design decisions

Each control in this repository exists because of a specific failure in real use, or a risk that was obvious once the
failure had been seen. Incidents are described without employer names. The table maps each failure to the relevant code
or prompt and its test coverage. Prompt-enforced controls depend on the assistant following instructions.

## Principles

1. **The model proposes; scripts and people dispose.** An assistant is good at drafting and bad at noticing that a sentence
   is unsupported. Deterministic checks catch the known mistakes; a person reads the final text.
2. **Fail closed on staleness.** A review, a batch spec and a persona each carry a revision or a hash. When what they point
   at changes, they stop working until someone looks, instead of quietly reusing old approval.
3. **Evidence is a ledger, not a resume.** Facts live once, with source, ownership and limits. Everything else is assembled
   from them. A generated document is never evidence.
4. **Humans own three decisions:** is the sourcing list right (Checkpoint A), which roles advance (Gate 1), and what is sent
   (Gate 2). The assistant never submits, signs in or sends a message.
5. **Planning limits warn; they do not erase records.** Refusing to log an application you already sent does not un-send it.
6. **Protect records.** Tracker writes use a lock, backup and atomic replacement. Events are appended after the tracker
   write. The skip list and handoff use simpler writes and should be backed up with the workspace.
7. **Personal data and code live apart.** Scripts read a workspace directory; applicant data belongs in an ignored workspace; public author attribution is separate.

## Failure modes and controls

| Failure mode | Control | Where | Test |
|---|---|---|---|
| A drafted resume line claimed more than the evidence supported: a modeled estimate was worded as a realized saving, and a contribution was stated that the evidence could not confirm. | Every line is a ledger claim with source, ownership and limits. A user-maintained rule list blocks a statement once caught. Qualified wording can clear a rule (`unless`). | `workflow_quality.content_issues`, `evidence/known_errors.json` | `ContentCheckTests` |
| A link supplied for one role opened a different posting at the same employer. On another occasion a posting URL later began serving a different role. | Title, link, team and requisition are verified together on the employer's own page; the full posting text is saved at sourcing. | `prompts/04_sourcing.md`, `05_triage.md` | (prompt-enforced) |
| Early batch specs carried their own copy of resume content, so a batch built from older specs could bring back superseded wording. | Schema v2: a batch spec selects a persona by ID and revision and may reorder its projects. Extra keys are rejected; a stale revision fails; a persona that loses a required claim is refused. | `workflow_quality.resolve_version`, `require_v2` | `EvidenceResolutionTests` |
| Duplicate applications happened, and links to one posting can differ only in tracking parameters. | URLs are normalized (tracking parameters and fragments removed, job identifiers kept); company + requisition is checked too. Duplicates are errors, not warnings. | `check_company.normalize_url`, `tracker_update` | `TrackerTests` |
| A posting that had been rejected at triage resurfaced in a later batch and cost review time twice. | An append-only skip list, matched by exact URL, consumed by sourcing. It is separate from the tracker so a rejection is not counted as an application. | `skip_list.py`, `sourcing.apply_filters` | `SourcingTests`, `WorkspaceAndHygieneTests` |
| A junior role was dropped because its description mentioned senior colleagues. | The seniority filter looks at the start of the title only. Years and preferred skills are judged in triage. | `config.excluded_title_patterns` | `SourcingTests` |
| A blank response in the tracker was read as a rejection, distorting the weekly review. | Outcomes are reported only for cohorts old enough to have responded; blank means "no recorded outcome". The report refuses causal claims. | `tracker_report.summarize` | `TrackerTests` |
| A per-company limit blocked logging an application that had already been sent. | Limits are planning warnings stored on the event. Duplicate URL or requisition stays fatal because it is a data-integrity error. | `tracker_update._new_application` | `TrackerTests` |
| An answer named a project the reader had never heard of and went straight to tools and numbers; its motive sentence repeated the employer's mission in stock wording. | A separate storytelling check: every project is introduced (kind, what, why) before detail; motive sentences are first person. The project list is user-maintained. | `workflow_quality.storytelling_issues`, `answer_check.py`, `prompts/09_storytelling_check.md` | `StorytellingTests` |
| Early letters followed one formula: company detail, a trust lesson, an analogy at greater scale, an apology for missing experience. | Editorial warnings (gap disclaimer, technical dismissal, contrast formula, analogy, moral comparison, adoption, personal reflection) require a recorded reason to keep. | `workflow_quality.EDITORIAL` | `ContentCheckTests` |
| A review that approved a draft could be reused after the text was edited. | A review stores the SHA-256 of normalized extracted text and the ledger revision; wording or ledger changes make it stale. Formatting still needs visual review. | `workflow_quality.validate_review` | `ContentCheckTests` |
| Aggregators showed a posting as new when the employer's own page showed it was weeks old. | Posting age is dated from the employer's own page where one exists; the age is recorded at triage. | `prompts/04_sourcing.md`, `employer_watch.py` (`date_source`) | `SourcingTests` |
| Hundreds of backup files accumulated next to the tracker, one per write. | Backups go to `backups/tracker/` and only the newest N are kept. | `tracker.Tracker._backup` | `TrackerTests` |
| The handoff log grew to hundreds of kilobytes and had to be read at the start of every session. | Keep it short; `archive_handoff.py` moves older entries to `history/` without deleting them. | `archive_handoff.py` | `WorkspaceAndHygieneTests` |
| One applicant-tracking parser attached a resume's Projects section to the previous job's description. | Section heading labels are configurable per user. | `base_resume.json` `style` | (manual) |
| An aggregator rate-limited a session that paged through results repeatedly. | One gentle pass per source per run; no retry loops; report and skip. | `AGENTS.md`, `docs/SOURCING.md` | (prompt-enforced) |

## Trade-offs

- **Strictness has a cost.** Registering every claim, purpose line and project alias takes real effort at setup. The payoff is
  later: batches become fast because nothing needs re-deriving.
- **Heuristics are blunt.** The storytelling and editorial checks use patterns. They produce false positives (resolve with a
  reason) and false negatives (the manual pass exists for those). They are not a quality score.
- **Files over a database.** Plain JSON and markdown keep the system inspectable, diffable and assistant-agnostic. The cost is
  that consistency is enforced by `doctor.py` and tests instead of a schema engine.
- **The assistant is trusted to read and follow the prompts.** Scripts enforce what can be enforced offline; the gates and the
  eligibility judgments depend on the assistant following `AGENTS.md`, which is why [LLM_COMPATIBILITY.md](LLM_COMPATIBILITY.md)
  is honest about having tested one assistant.

## Operational limits

- Approval flags and review notes are editable records, not authenticated human consent. The scripts do not control
  your assistant's desktop permissions. Submission stays with the user through the interaction rules.
- Tracker writes are locked, but duplicate checking happens before the write lock. Run one logging session at a time;
  concurrent writers could validate against the same old state. The tracker and event log are not one transaction.
- The simpler skip-list and handoff writes are intended for one local user. Back up the private workspace.
- Source adapters and Python regressions are tested with fixtures. Live API availability and assistant behavior require
  separate evaluation; no passing unit test establishes application accuracy or job-search effectiveness.
