# 06 - Tailoring and the application set

Run after Gate 1 (you chose the roles). The assistant picks a persona per role, produces the final list for you to apply
from, and drafts what the applications require. **You** review, correct and submit everything yourself (Gate 2).

---

Tailor the roles I approved: [list them, or "the roles I approved in today's triage"].

## Steps
1. **Persona per role,** by the actual core function of the job, not keyword overlap. Do not rename a persona and call it
   tailored. If no persona fits, say so and propose a new one built from evidence (`prompts/03_personas_and_resumes.md`).
2. **Reorder only.** A project may be reordered for a role (`project_order`); content never changes in a batch. A bullet
   that needs to change changes in the ledger and the personas that use it, with a new `revision`.
3. Write the batch spec (`resume_versions/<date>_<label>.json`, schema_version 2, `canonical_revision` current), then
   `python3 scripts/resume_generator.py --spec <spec> --dry-run`, then generate once the spec has `"approved": true`.
4. For each role list the requirements my evidence does **not** cover (for interviews; never added to the resume).
5. **Visible application questions:** read the application form if you can see it (without signing in or submitting).
   Draft an initial answer for each question from my evidence, interests, motives and previous answers
   (`prompts/07_letters_and_answers.md`). Standard fields (sponsorship, start date, salary, relocation) get truthful answers
   from my profile; salary and personal fields are mine to confirm.
6. **Cover letters:** optional by default. Say clearly when a posting **requires** one. Draft one only when required, when I
   ask, or when my profile says so.

## Output in the reply (and in `batches/<date>_grouping.md`)
- The list of resume documents, **ordered by how many roles each serves, fewest first**, and under each document its
  roles, each with the **full live posting link**.
- Required materials per role, deadlines, and the questions you could not see (I will bring them later, one at a time or in
  a batch).
- What is unresolved and needs me.

Then run the review (`prompts/08_review.md`) on every new or changed document and answer. Nothing is sent. I check the
quality, correct anything, then apply myself. When every application is submitted or skipped, I tell you and we log them
(`prompts/10_logging_and_weekly_review.md`).
