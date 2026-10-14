# The evidence model

Everything an assistant writes about you comes from one place: the evidence ledger. This document defines its fields, how
personas and batches are built from it, and how revisions keep old work from being reused silently.

## The ledger: `evidence/claims.json`

```json
{
  "revision": "2026-01-05.1",
  "change_note": "why this revision exists, and what the previous one was",
  "claims":      { "<id>": { ... } },
  "reflections": { "<id>": { ... } },
  "credentials": { },
  "languages":   { },
  "unresolved":  ["open questions to answer next time"]
}
```

### A claim

| Field | Meaning |
|---|---|
| `text` | one resume-ready sentence: what it was and what you did, then tools and numbers; past tense, concrete |
| `source` | where the fact comes from: your own answer with its date, a report, a review. "The resume" is not a source |
| `ownership` | `personal`, `shared with <who>`, or `team result`. Team credit never becomes personal credit |
| `limitations` | what must not be claimed and the scope of any number (what was counted, over what, against what baseline) |
| `status` | `usable` (may appear in materials), `needs_confirmation` (not yet), `retired` |

Rules: one fact per claim; shared work says so in the text ("co-built"); numbers keep their scope; a prototype is not
production, a pilot is not adoption, a public site is not users; coursework is not professional experience.

### Purpose claims
When its purpose is confirmed, a project has a `<project>.purpose` claim saying why it existed (the client's goal, or your own
reason). Resumes print it as an italic line under the project title. It must be a real, recorded reason; if there is none, the
project shows no purpose line. A purpose never implies adoption or deployment.

### Reflections
Motives and personal details **in your own words, with the date**: what work you want next and why, what you want to avoid, a
project you are proud of. They are the only motives a letter or answer may use. The assistant never infers a motive from a project.

### Learning from your edits
When you edit a draft and add a true statement, it is a fact about you. Your choice in `PROFILE_AND_RULES.md` section 7 decides
whether the assistant adds it to the ledger (with date and source) and reuses it without asking, or asks first. The ledger limits
still apply: no usage, adoption or deployment claim you have not stated.

## Companion files in `evidence/`

- **`BOUNDARIES.md`**: the specific ways a statement could overreach, with what is supported instead.
- **`known_errors.json`**: regex rules that block statements once caught. `unless` lets qualified wording through.
- **`project_aliases.json`**: regexes that tell the storytelling check which names are projects or clients.

## Personas: `canonical_resumes.json`

```json
{
  "revision": "2026-01-05.1",
  "change_note": "...",
  "profiles": {
    "DataAnalytics": {
      "family": "data_analytics",
      "core_positioning": "one sentence on what this persona shows",
      "skills": [{"group": "Analysis", "items": ["Python", "pandas", "SQL"]}],
      "projects": [
        {"id": "bikeshare", "title": "Bike-Share Demand Forecast - Course Capstone",
         "claim_ids": ["bikeshare.how", "bikeshare.result"], "purpose_id": "bikeshare.purpose"}
      ],
      "required_claim_ids": ["bikeshare.result"],
      "coursework": "Relevant coursework: Regression Analysis, Databases"
    }
  }
}
```

A persona is a job family, not a company. Bullets are never typed into it: they are ledger claims, in order (how, then result).
`required_claim_ids` are claims the persona must always show; a persona that loses one is refused. `status: "retired"` (with a
`retired_note`) takes a persona out of use without deleting it.

## Batch specs: `resume_versions/<date>.json`

```json
{
  "schema_version": 2,
  "batch": "2026-01-06_demo",
  "approved": true,
  "versions": [
    {"canonical_id": "DataAnalytics", "canonical_revision": "2026-01-05.1", "label": "DataAnalytics",
     "job_family": "data_analytics", "companies": ["Acme"], "target_jobs": ["Data Analyst I - 1003"],
     "project_order": ["pantry", "bikeshare"]}
  ]
}
```

Only those keys are allowed. `approved` records your Gate 1 choice; the generator refuses to write files without it (dry-run
works without). A spec naming a stale `canonical_revision` fails.

## Reviews

A review object (`templates/specs/review.EXAMPLE.json`) records who checked what and ties the check to extracted text with a SHA-256
digest after whitespace normalization and the ledger revision. It lists claim checks (statement, source, scope check, optional claim ID), the verified company
sources, specific notes on role match, voice and proofreading, and a concrete reason for every editorial warning that was kept.
Change the wording and the digest no longer matches; formatting and whitespace alone are not covered; change the ledger and the revision no longer matches.

## Changing the ledger or a persona

1. Verify the source. 2. Edit the claim or persona. 3. Write the reason in `change_note`. 4. Increase `revision`.
5. `python3 scripts/doctor.py`. 6. Update any batch spec you still need to the new revision. Do not rewrite a whole catalog to
suit one batch, and do not relax a check to make an old batch pass.

## What Python enforces

Project bullets and optional purpose lines resolve from usable claim IDs. Stable professional-experience bullets
must match usable claim text. Persona revisions, review digests and known-error patterns are checked mechanically.

Contact details, education, titles, dates, skills and coursework remain text fields. A review must check them against
the ledger, but Python does not automatically establish a source for each field. Likewise, review objects are recorded
assertions, not proof that the checks were performed. Never treat a passing command as approval to submit.
