# 07 - Cover letters and screening answers

Use for required or requested letters and for every written answer on an application. Applications may show more
questions as I go: bring them to the assistant one at a time or in a batch and it drafts those the same way.

---

Draft [a cover letter / answers to these questions] for [company, role]. Read `VOICE.md`, `PROFILE_AND_RULES.md`,
`evidence/BOUNDARIES.md`, `evidence/claims.json`, the saved posting and the resume I am sending. The exact questions
and any limits are below.

## Before drafting
- Name the two or three central needs of the role from the posting; find my evidence for each (claim IDs). One or two
  experiences are enough; do not walk through the resume.
- For "why this role / company": use only motives recorded in my ledger `reflections`. If none fits, ask me **one** focused
  question and record my answer there. A professional interest in the actual work is enough; never invent a lifelong
  connection, a story or admiration.
- A company fact needs a named source (the posting, the company site, a dated article) and a sentence that ties it to my
  own evidence. Skip company news that does not connect to what I did.
- Reuse earlier answers and edits only after their factual statements have been confirmed and recorded in the ledger.
  Sending an answer does not make it evidence.

## Letters (optional unless required)
One through line, in this order of preference: (1) a true personal story from my ledger that explains my interest;
(2) a recent verifiable company development tied to something I did; (3) otherwise the needs-to-evidence structure
(opening, one sentence naming the two or three needs I meet, one short paragraph per need leading with the need). Usually
180-300 words; shorter when complete; employer limits override. No posting summary, no default gap paragraph, no apology.

## Short answers
Open directly. A "why" is answered in its first words. Give the reason behind a claim and the action that followed. Define a
term the first time it appears. End on what I would do for the team. Cut technical detail before cutting the introduction
when a word limit is tight.

## Rules for everything
- **Introduce every project** the first time it appears: what kind of thing it was and where it came from, what it did in
  plain words and for whom, why it existed; only then tools and numbers. Each answer is read on its own.
- Keep team credit and number scope exactly as in the ledger. No moral lessons, no peer comparisons, no inflated claims.
- Standard questions (sponsorship, start date, salary, relocation, authorization) are answered truthfully from my profile;
  never shade an eligibility answer. Salary and personal fields are mine to confirm.
- If an employer states a rule about AI-assisted applications, quote it and tell me before I use a draft.

## Output
1. Each draft as a blockquote under its question (so `answer_check.py` can read it), with word and character counts.
2. A short note for me, not the employer: which needs, which claim IDs support each sentence, what to confirm.
3. Run `python3 scripts/answer_check.py <file>` and `prompts/09_storytelling_check.md`, then review (`prompts/08_review.md`).

If I edit a draft, compare it with your version: each new statement is a fact about me. Per my profile, add it to the
ledger with its date and source (or ask me first), and reuse it later where relevant. Re-review after every edit.
