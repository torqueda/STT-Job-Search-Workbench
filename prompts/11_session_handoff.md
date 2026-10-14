# 11 - Ending a session

Assistants forget between conversations. The files are the memory, so every session ends by writing down what happened.

---

Let's wrap up. Do all of this in the workspace, then summarize it for me:

1. **Update the files that changed:** `PROFILE_AND_RULES.md` (any rule or preference I stated today, dated, in my words),
   `VOICE.md` (a lasting writing correction), `evidence/claims.json` (new grounded statements, with `revision` and
   `change_note`), `evidence/known_errors.json` (a mistake we caught), `config.json` (exclusions, limits), and the tracker.
2. **Add a `HANDOFF.md` entry** at the top:
```
## YYYY-MM-DD
Done: (what we did, briefly)
Decisions: (roles approved or skipped, rule changes, with my words where it matters)
Submitted: (company - title - resume version), or "none yet"
Pending: (waiting on me or on an employer)
Deadlines: (date - company - what)
Open questions:
```
3. Run `python3 scripts/doctor.py` and `python3 -m unittest discover -s tests` if scripts or the ledger changed. Report failures; do not hide them.
4. If `HANDOFF.md` is over about 300 lines, run `python3 scripts/archive_handoff.py`.
5. List anything that needs me before the next session.

Tips: start a fresh conversation for each session; if the assistant contradicts the files, the files win; keep dated copies
of the ledger before big edits (`backups/`).
