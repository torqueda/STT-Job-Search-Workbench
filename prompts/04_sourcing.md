# 04 - Sourcing (Checkpoint A)

The assistant finds postings; **you** check that the list is satisfactory before it triages anything. Run at the
frequency in `PROFILE_AND_RULES.md` (many people source every day or two; postings fill quickly).

---

Source postings for me today. Read `PROFILE_AND_RULES.md`, `config.json`, `tracker.csv` (or my tracker), and
`skipped_listings.json` first. Read `docs/SOURCING.md` for the sources I have enabled.

## Sources
1. **Open sources, no login:** the community feed set in `config.json` (`python3 scripts/sourcing.py --role-profile <label>
   --source github --hours 24`) and my employer watchlist (`python3 scripts/employer_watch.py --days 2`).
2. **Links or text I paste** (any board, a referral, an email): save the full text and treat it as a lead.
3. **Boards that need my login:** only if I ask and I am signed in myself, in a browser you can see. Follow the site's
   terms; read what is on screen, one gentle pass, no repeated paging. Never type my credentials, sign in for me, solve a
   captcha, or like/save/apply/change filters on any site. If a site shows a captcha, a rate limit or asks for sign-in,
   report it and skip that source. See `docs/SOURCING.md`.

## For every posting kept
- Find it on the **employer's own site** (an aggregator is a lead, not the employer). Confirm the title, link, team and
  requisition ID belong together. If the link opens a different role, say so.
- Save the full posting text to `job_descriptions/` (postings get taken down) with the requisition ID.
- Drop what is already in my tracker or skip list, excluded companies, and roles outside my allowed countries or other scope rules.
- Posting age: apply my sourcing age limit, dating from the employer's own page where possible.

## Output
A list grouped by job family: company, exact title, location, posting date, employer link, one line on why it may fit,
and what you dropped and why. Say which sources worked, which were skipped (signed out, rate limit) and anything odd.

**Then stop.** I review the list. Only when I say "go ahead" do you triage (`prompts/05_triage.md`).
