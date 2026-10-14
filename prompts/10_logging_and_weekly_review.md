# 10 - Logging applications, and the weekly review

Two parts: logging (after you finish a batch, and whenever you hear back) and a weekly review.

---

## Part A - Logging

I have [submitted these applications / skipped these / heard back from these companies]: [details].

Rules:
- Log an application **only after I confirm I submitted it**, with the date I submitted. Skipped roles go to the skip list
  (`scripts/skip_list.py`), not the tracker. Unknown dates and outcomes stay blank; never fill what I have not told you.
- New application: `python3 scripts/tracker_update.py --title ... --company ... --link ... --requisition-id ... --date YYYY-MM-DD
  --confirmed-submitted --resume-spec resume_versions/<spec>.json` (or `--package <dir>`). Run it first with `--dry-run` and
  show me the row. A repeated URL or company + requisition is a duplicate: update the existing row.
- Status values: Submitted, Screening, Assessment, Interview, Offer, Rejected, Withdrawn (and Ghosted only after 45+ days of
  silence and only if I say so). An update needs its actual stage date; a rejection is dated the day I report it unless I give
  another. `python3 scripts/tracker_update.py --update-row N --status Interview --stage-date ... --interview-date ...`.
- A company over its limit is a planning warning: log what I actually sent.
- For interviews and assessments add the date and a next action ("prepare by Friday").
- If I used a different tracker (Excel, a sheet), update that one the way `config.json` says, and show me what changed.

## Part B - Weekly review (about 15 minutes)

Run `python3 scripts/tracker_report.py` and tell me:
1. **Volume:** applications this week and last, versus my weekly target.
2. **Outcomes by cohort:** only for applications at least 30 days old; share with any response, screening, interview or offer,
   by job family, fit (Good vs Stretch), source and referral. Say plainly when samples are too small to mean anything.
3. **What is working** (sources, families, employer types) and **what is not** (fast rejections, silent families).
4. **Whether stretches are crowding out Good matches.**
5. **Changes to consider** next week. I decide; record decisions in `PROFILE_AND_RULES.md`.
6. **Follow-ups due:** interviews to prepare, thank-you notes, applications worth a polite follow-up.

A blank response means unknown, not rejection. Never claim that one element (a letter, a persona) caused an outcome.
