# Handoff log

The assistant's memory between sessions. A new conversation knows nothing about the last one except what is
written here and in the other workspace files, so every session ends with an entry.

Newest entry at the top. Keep this file short: it is read at the start of every session. When it passes about 300
lines, run `python3 scripts/archive_handoff.py` to move older entries to `history/`.

## YYYY-MM-DD
Done:
Decisions: (roles approved or skipped, rule changes, with your words where it matters)
Submitted: (company - title - resume version), or "none yet"
Pending: (waiting on you or on an employer)
Deadlines: (date - company - what)
Open questions:
