# 09 - Storytelling check for every suggested answer

Run on **every suggested screening answer, letter paragraph, outreach message and email** before the facts review in
`08_review.md`. It is a separate, recorded pass. It does not apply to resumes, whose project blocks carry registered
purpose lines.

The reason it exists: a drafted answer named a project the reader had never heard of and went straight to its tools and
numbers, and its motive sentence repeated the employer's mission in stock wording. The applicant had to repair both by hand.

Read `VOICE.md` and `evidence/claims.json` first.

## 1. Run the mechanical check
```sh
python3 scripts/answer_check.py <answers-file.md>        # every blockquoted answer
python3 scripts/answer_check.py --text "<one answer>"
```
It flags a project named without what kind of project it was or why it existed (`project_intro`), "systems like this" with no
antecedent (`vague_referent`), the employer's mission paraphrased in stock wording (`employer_mission`), and stock phrases
(`stock_phrase`). It only knows the projects registered in `evidence/project_aliases.json`. Fix each flag, or record a specific
reason under `warning_resolutions`. A clean run proves nothing about the story: do the manual pass anyway.

## 2. Manual pass, for each answer
Read it as a stranger who has never seen the resume, the folder or the posting.

1. **Introduce every project, system or client the first time it appears,** before any tool, number or result: what kind of
   thing it was and where it came from (personal, course, capstone, hackathon, job; solo or team); what it did in plain
   words and for whom; why it existed (the registered `<project>.purpose` claim or my recorded motive; if the ledger has
   none, describe the work without a purpose or ask me, never invent one). Organizations get the same treatment. This holds
   even when the same project was introduced in another answer on the same form: each field is read on its own.
2. **Say what the thing was for, not only what was done,** using only purposes I have recorded.
3. **Give the reason behind a claim** and the action that followed, using only reasons and actions I have stated.
4. **Define a term the first time it is used** (one clause).
5. **Motive sentences are about me, in first person:** my growth, the responsibility I want to own, the specific work. Do not
   restate the employer's mission or describe the employer as "a team that is turning X into Y". No "systems like this"
   unless the antecedent is in the same sentence.
6. **A "why" question is answered in its opening words** ("Because ..."), not after a summary of the posting.
7. **Check each introduction against the ledger limits:** team vs personal credit, "built" vs "deployed" vs "used by", and
   `BOUNDARIES.md`. An introduction that makes the project sound more deployed or adopted than it was is a defect.

## 3. Record the result
In the review file add a **Storytelling check** table:

| Answer | Projects and organizations named | Introduced (kind, what, why) and source claim | Motive sentence checked | Flags resolved |
|---|---|---|---|---|

Do not fill the table from a clean run. For letters and packages, `validate_review(..., writing=True)` runs the same flags
and refuses a review that leaves one unresolved.

## Before and after (fictional)
- Before: "I built Shelfbot with Python."
  After: "Shelfbot was a personal project to help library visitors find shelf locations. I built a Python prototype
  that matched book titles to a sample catalog; it was not deployed in a library."
- Before: "I want to build systems like this for a team that is turning data into decisions."
  After: "I want to work on data validation because I enjoyed tracing catalog errors in that project."

These invented examples illustrate structure only. The project, purpose, scope and motive would each need a ledger
source before appearing in a real application.
