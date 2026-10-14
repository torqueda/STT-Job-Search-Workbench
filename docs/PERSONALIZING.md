# How the system grows with you

You do not need a perfect first setup. The workflow is designed so that every correction you make is written down once and applied
from then on. Expect the files to change a lot in the first weeks.

## The learning loop

| You do this | The assistant writes it here |
|---|---|
| State a lasting preference or exclusion ("never apply to gambling companies", "hold roles under my salary floor") | `PROFILE_AND_RULES.md` change log, dated, in your words; `config.json` for exclusions and limits |
| Correct how a draft sounds ("open with the reason", "never say passionate") | `VOICE.md` preferences, dated |
| Edit a drafted answer, adding something true about your experience | `evidence/claims.json` (with date and source), then reused where relevant. Your choice in `PROFILE_AND_RULES.md` section 7: add without asking, or ask first |
| Catch a factual mistake in a draft | a rule in `evidence/known_errors.json` so it cannot return |
| Mention a new project or client | `evidence/project_aliases.json`, so the storytelling check can see it |
| Say a persona is wrong or a bullet should change | the ledger claim first, then the persona; increase `revision` and write a `change_note` |
| Overrule a triage verdict | the decision noted in `HANDOFF.md`; a pattern becomes a rule in `PROFILE_AND_RULES.md` |

## What tends to emerge (from my own use)

- **Industries or employers you never want**, which only show up when a posting lands in front of you.
- **A consistent tone for answers**, grounded in what you really did: a direct opening, the reason behind a claim, an ending on
  what you would do for the team.
- **Rules about how to count experience**, for example how much your degree counts when a posting states years. These decide which
  roles you pursue; your materials stay truthful.
- **Which sources are worth the time**, and the pace at which you can actually apply.
- **Corrections to resumes you always make** (a header detail, a hyphen instead of a dash). Tell the assistant once; it can match
  your habit in the next draft.

## Adding and retiring personas

A new job family is a new persona built from evidence, never a renamed copy of an existing one. Retire a persona by setting
`"status": "retired"` (and a `retired_note`) rather than deleting it; old specs then fail with a clear message. Remove a retired
persona only when no spec you need refers to it.

## Tuning the checks

- `config.json` -> `editorial_checks_disabled` switches off a built-in editorial warning you find unhelpful (the keys are in
  `workflow_quality.EDITORIAL`). Prefer resolving a warning with a reason over disabling it.
- `config.json` -> `letters` sets word limits, optional required opening/closing sentences and extra banned phrases.
- `config.json` -> `resume_limits` sets content limits that produce warnings and `max_pages` (default 1), enforced when packaging a resume.
  Keep `max_pages` consistent with your profile. The user records the final page count after inspection.

## Keeping the files healthy

This updates the context the assistant reads; it does not train or fine-tune a model. A factual correction must
be supported by the ledger before it can be reused.

Run `python3 scripts/doctor.py` after any edit to the ledger, personas or regex files, and `python3 scripts/archive_handoff.py` when
`HANDOFF.md` gets long. Keep dated copies of the ledger before large edits (`workspace/backups/`).
