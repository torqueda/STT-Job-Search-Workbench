# Application identity and limits

How the scripts and the assistant decide whether an application is a duplicate, what counts toward a limit, and
what may be logged. These are defaults with reasons; change a rule only on purpose and record it in the change log
of `PROFILE_AND_RULES.md`.

## Identity
- A posting is identified by its normalized URL (tracking parameters removed, job identifiers kept) and, within a
  company, by its requisition ID. Different genuine requisitions in the same job family are not duplicates.
- Verify title, URL, team and requisition together on the employer's own page. A link supplied for one role has
  resolved to a different posting before; aggregators are leads, not the employer.

## Limits
- Company limit: N applications to one company inside a rolling window (default 2 in 60 days). Incomplete attempts
  do not count.
- Caps govern planning, not recording. Refusing to log an application you already sent does not un-send it; it only
  loses the record. An exceeded cap is a PLANNING CAP WARNING stored on the event.
- A repeated normalized URL, or a repeated company plus requisition, is a data-integrity error and stays fatal. Use
  `--update-row` instead of recording twice.
- No daily volume cap by default. Volume is never a reason to advance a poor match.

## Logging
- Log only after you confirm you submitted. Record the package or the approved spec that produced the resume.
- A stage change needs its actual date. A rejection is dated the day you report it unless you give another date.
- A blank response means unknown, not rejection. Never fill in dates or outcomes you have not given.
- One writer at a time; every write is preceded by a backup and is atomic. Events are appended to
  `application_events.jsonl`.

## Eligibility
- Eligibility (authorization, clearance, citizenship, start and graduation windows, location) is decided separately
  from fit, from the exact posting language. Unknown is not eligible.
- Active clearance is different from the ability to obtain one.

## Change log
- YYYY-MM-DD:
