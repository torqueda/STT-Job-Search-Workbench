# 03 - Personas and resumes

A persona is a job family you apply to (for example Data Analytics, ML Engineering, Product Analytics) with its own
resume. Applications reuse a persona; they do not get one-off rewrites. Use this after the evidence ledger exists.

---

Build my personas and their resumes. Read `PROFILE_AND_RULES.md` (targets), `evidence/claims.json`,
`evidence/BOUNDARIES.md` and `docs/EVIDENCE_MODEL.md`.

## Rules
- Choose content by the **core function** of the job family, not by keyword overlap. A data-engineering persona leads
  with pipelines and reliability; an analytics persona leads with analysis and decisions.
- A persona is a record in `canonical_resumes.json`: skill groups (2-4), 2-3 projects (each: `claim_ids` for its bullets
  and a `purpose_id` when its purpose is confirmed), `required_claim_ids`, `core_positioning`, `family`. Every bullet is a `usable` ledger claim. If a
  persona needs something the ledger lacks, add it to the ledger first (with its source), never to the persona.
- Each project shows a confirmed purpose line when available, then a how bullet (tools and techniques), then a result bullet (measured outcome
  or decision, never assumed impact).
- Stable identity, education and experience live in `base_resume.json`; every experience bullet must also be a ledger claim.
- No summary or objective unless I ask. No invented metrics, no skills I cannot discuss in an interview.
- One page unless my profile says otherwise: cut low-value content before reducing type size.

## Process
1. Propose the personas (one per job family in my targets) and, for each, the 2-3 things it must show. Wait for my approval.
2. Draft one persona at a time. After each: which claims you used and why, which you left out and why, and the gaps my
   evidence does not cover (to handle honestly, not to fake).
3. Write the approved personas into `canonical_resumes.json` (increase `revision`, add a `change_note`). Run
   `python3 scripts/doctor.py`.
4. Generate previews with a batch spec (`templates/specs/resume_spec.EXAMPLE.json`):
   `python3 scripts/resume_generator.py --spec resume_versions/<name>.json --dry-run`, then without `--dry-run` once the
   spec has `"approved": true`.
5. I open each DOCX and finalize it my own way (see `docs/RESUME_HANDLING.md`). You do not export PDFs or count pages.

## Later changes
Improve a bullet by fixing the ledger claim first (with the reason and date), then the personas that use it. Increase
`revision`: older batch specs fail as stale on purpose. A new job family gets a new persona built from evidence, never a
renamed copy of an existing one.
