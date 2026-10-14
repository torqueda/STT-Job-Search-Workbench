# 05 - Triage (Gate 1)

Run after you approved the sourcing list. The assistant labels every role Good, Stretch or Poor, and says why. **You**
choose which roles advance, and you may change any role's fit.

---

Triage the approved postings. Do not tailor anything. Read `PROFILE_AND_RULES.md`, `APPLICATION_POLICY.md`,
`evidence/BOUNDARIES.md`, `evidence/claims.json`, `canonical_resumes.json`, the saved postings, the tracker and the skip
list. A resume or letter is never evidence.

## For each posting
1. **Real and open?** Read the full posting at the employer's site. Record company, exact title, requisition ID, link,
   location and arrangement, pay if stated, posting date and age. Closed, gone, or title/link/ID mismatch: say so.
2. **Duplicate or limit?** `python3 scripts/check_company.py "<company>" --url <link> --requisition-id <id>`. The company
   limit is a planning warning; a repeated URL or requisition is a duplicate.
3. **Eligibility, separately from fit.** Quote the exact posting language on authorization/sponsorship, citizenship,
   clearance and export control, start date, graduation or enrollment window, location. Apply my rules: `clear`,
   `blocked` or `unknown` (unknown is never eligible: say what to verify). Preferred skills or years are not mandatory ones.
4. **Fit.** Name the three central responsibilities. Map each to my evidence: direct (claim IDs), adjacent, coursework
   only, or missing. No numeric score pretending to be a probability.
5. **Verdict.**
   - **Good**, **Stretch** or **Poor**, with the reason in a sentence.
   - For a Stretch: the main gap, and whether it is a **skill stretch** (a trainable tool or domain) or a **level stretch**
     (seniority, years, leadership or architecture scope).
   - Priority: apply now / selective stretch / verify first / skip.
   - Persona: which one, and why (by core function, not keyword overlap).
   - Materials: is a cover letter or written answer **required**, **optional** or absent? Any employer rule about AI use?
   - Contact route only as the posting names it ("not named" otherwise).

## Output
1. **Repeats.**
2. **Recommended:** a table (company, title, location/pay/age, fit with reason, persona, link). Good first, then
   stretches, kept to my stretch share, skill stretches before level stretches. Level stretches are listed and marked skip
   unless there is a referral.
3. **Verify first:** eligibility unknowns with the exact thing to check.
4. **Eligible but not recommended:** with the reason (below pay floor, company at limit, weak fit).
5. **Blocked** with the quote; **Poor fit**; **closed or not found**.
6. Deadlines.
7. Skip-list entries for blocked, poor-fit, closed and level-stretch roles, ready to run through `skip_list.py` once I
   confirm.

**Then stop.** Tell me which roles to advance and any fit you would change. Record my choice (and any rule change in my
words) in `HANDOFF.md` and `PROFILE_AND_RULES.md`. Only then tailor (`prompts/06_tailoring.md`).

## Reminders
- A title alone never decides fit; read the duties. "No minimum years stated" does not mean entry level.
- Do not write off a good match for one missing tool; say what is missing.
- If I overrule a verdict, go with it and note it.
