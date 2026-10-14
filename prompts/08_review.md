# 08 - Review before sending

Run on every resume that changed, every letter and every written answer, right before I send it. The review is a fresh
look at the actual final text, not a defence of the draft.

---

Review this [resume / letter / answer] for [company, role]. Read `VOICE.md`, `evidence/BOUNDARIES.md`,
`evidence/claims.json` and the saved posting. Check, in this order:

## 1. Facts
Sentence by sentence, give the ledger claim ID each statement rests on, or mark it **unsupported**. Check ownership
(personal vs team), number scope and denominator, chronology, limits; that no tool, certification, title or date appears
that is not in the ledger; that motives come from `reflections`; that company claims have a named source and connect to my
evidence; and that nothing confidential is included.

## 2. Role match
Use the saved posting (company, title, requisition, team, central duties). Does the document show evidence for the central
needs, most important first? For letters, is there one through line, with posting summaries and standalone company news
cut? Does every project introduction work for a stranger?

## 3. Voice
Check against `VOICE.md`: generic trust narratives, apologies, technical dismissal, unsupported analogies, peer
comparisons, padding. Would I naturally say each sentence?

## 4. Proofreading
Names, company, title, dates, grammar, duplicated words, tense, punctuation, flow.

## 5. Form
Letters and answers within limits. Resumes: I check the exported PDF's page count and layout myself.

## Recording the review
`python3 scripts/workflow_quality.py <file> [--writing]` prints the text digest and the automatic checks. A review object
(`templates/specs/review.EXAMPLE.json`) records: `text_sha256`, `evidence_revision`, `reviewer`, `reviewed_at`,
`claim_checks`, `company_sources`, `role_match`, `voice`, `proofreading`, and `warning_resolutions` (a concrete reason for
every flag you keep). Never fill positive notes from a clean automatic run. A review digest covers extracted text with whitespace normalized. Wording edits,
including mine, make it stale and require a new review. Formatting changes require a fresh visual check.

## Output
**Must fix** (unsupported or wrong statements, with the fix), **should fix**, **typos**, and a one-line verdict: ready, or
ready after the must-fix items.
