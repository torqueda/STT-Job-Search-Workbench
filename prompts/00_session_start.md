# 00 - Start of every session

Paste or point your assistant to this at the start of each working session (a fresh conversation each time works
best: the files, not the chat, are the memory).

---

We are starting a job search session. Read `AGENTS.md` first, then, from my workspace folder (`workspace/` unless I
say otherwise):

1. `PROFILE_AND_RULES.md`, `VOICE.md`, `APPLICATION_POLICY.md`
2. `evidence/BOUNDARIES.md` and `evidence/claims.json`
3. the newest entries of `HANDOFF.md`
4. `config.json`

If the workspace does not exist or `PROFILE_AND_RULES.md` is still the blank template, stop and run the initial
setup instead (`prompts/01_setup_interview.md`).

Then tell me, in five lines or fewer: what is pending, any deadline in the next 7 days, and any open question for
me. Flag anything overdue (interviews to prepare, follow-ups). Run `python3 scripts/doctor.py` and report any error.

Then wait. Today I want to: **[source / triage / tailor / draft answers / log what I submitted / weekly review / other]**.

---

Notes
- If the assistant contradicts the files, the files win. Tell it to re-read them.
- No file access (a plain chat)? Attach the workspace files and see `docs/LLM_COMPATIBILITY.md` for what changes.
