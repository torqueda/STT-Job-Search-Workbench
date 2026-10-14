# Tracking

## The tracker

One row per submitted application. Choose CSV (default, opens in any spreadsheet) or an Excel workbook in `config.json`.

| Field | Meaning |
|---|---|
| Date applied | the date you actually submitted |
| Company, Job title, Type, Location, Link, Requisition ID | identity of the posting |
| Job family, Fit, Source, Referral | for the weekly review (Fit is Good or Stretch as you confirmed it) |
| Resume version | the persona (and revision) that produced the resume |
| Application package | path of the frozen package, or a note when you exported the PDF yourself |
| Status | Submitted, Screening, Assessment, Interview, Offer, Rejected, Withdrawn, Ghosted; `Incomplete - ...` for an attempt that did not finish |
| Stage date, First response date, Interview date | actual dates only; blank stays blank |
| Next action, Notes | free text |

Row numbers are the numbers you see in a spreadsheet (the header is row 1 for CSV), and `--update-row N` uses them.

## Rules

- Log only after you confirm submission and supply its actual date (`--date YYYY-MM-DD`). Never invent a date or an outcome.
- A new row needs evidence of what was sent: a package (`--package`), or the approved batch spec that produced the resume
  (`--resume-spec`). A spec records the persona label, not the exact final file or proof that it was reviewed;
  prefer a package when you need a record of the submitted bytes.
- A repeated normalized URL, or a repeated company + requisition, is rejected: update the existing row instead.
- The company limit warns (`PLANNING CAP WARNING`) and is stored on the event; it never blocks recording.
- A stage change needs `--stage-date`; a rejection defaults to today.
- `Incomplete...` attempts do not count toward the limit.

## Safety

Each write: a lock file stops a second writer; the file is copied to `backups/tracker/` (newest `backup_keep` kept, default 30);
the new file is written to a temporary name and swapped in; an event is appended to `application_events.jsonl`. If the event
append fails after the tracker was saved, the event is preserved in a `.pending-event.json` file and the command tells you not to
append it again.

## Excel

```json
"tracker": {"format": "xlsx", "path": "My Applications.xlsx", "sheet": "Sheet1", "header_row": 2,
            "columns": {"date": "A", "company": "B", "job_title": "C", "link": "F", "status": "N"}}
```
Only the fields you list are read and written; missing headers are added; every other cell and sheet is left alone. Close the
file in Excel before a write.

## The report

`python3 scripts/tracker_report.py [--minimum-age-days 30] [--as-of YYYY-MM-DD]` groups applications old enough to have heard back by
job family, source and fit. A blank outcome is "no recorded outcome", never "rejected". The cohorts are small and not random, so
the report makes no causal claim about letters, resumes or sources.
