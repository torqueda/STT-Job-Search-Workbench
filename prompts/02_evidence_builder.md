# 02 - Build the evidence ledger

Use after the setup interview; it may take two or three sessions. The ledger (`evidence/claims.json`) becomes the
only source of facts for every resume, letter and answer, so accuracy matters more than polish.

---

Build my evidence ledger from my resume, portfolio, coursework and a guided interview. Read
`docs/EVIDENCE_MODEL.md` first for the exact fields.

## Step 1 - Inventory
List every job, internship, project, publication, award, course project and credential you found, with dates. Ask what
is missing (side projects, open source, research, teaching, volunteering, languages). Agree the list with me first.

## Step 2 - One entry at a time
Most recent and most relevant first. For each, ask only the questions that apply, then write the claims.

- **Context:** what was the organization, team or client; why did the work exist; was it a job, internship, course
  project, capstone, hackathon or personal project; team size; dates.
- **What I personally did:** what I built, decided, analyzed or owned myself; what others did; which tools I used
  hands-on, and which I only saw others use.
- **Results:** what changed; numbers with exactly what was measured, over what period, against what baseline, by whom;
  whether it shipped, stayed a prototype or was handed off; who used it (only if I can say so firsthand).
- **Limits:** what must never be overstated ("prototype, not production", "team result", "estimate, not measured",
  "my share was the pipeline only"); anything confidential and how it may be described.
- **Why it existed:** in my words, the client's goal or my own reason. This becomes the `<project>.purpose` claim, the
  italic line under the project on a resume. If I have no reason to give, record none; never invent one.

## Step 3 - Write the claims
For each entry write 2-6 claims plus a purpose claim for each project whose purpose I confirmed, directly into `evidence/claims.json`:
`text` (one resume-ready sentence, past tense, concrete: what it was and what I did, then tools and numbers),
`source` (my answer with its date, a report, a review), `ownership` (personal / shared with whom / team result),
`limitations`, `status` (`usable`, or `needs_confirmation` when uncertain, and add it to `unresolved`).
One fact per claim; shared work says so ("co-built", "as part of a four-person team"). Increase `revision` and write a
`change_note`.

## Step 4 - The rest
- `reflections`: motives and personal details **in my own words, with the date** (what work I want next and why, what
  I want to avoid, a project I am proud of). These are the only motives letters and answers may use.
- `credentials` (exact names, only ones I hold) and `languages`.
- `evidence/BOUNDARIES.md`: the specific ways a statement could overreach (a dataset size that is not "processed", a
  public site that is not "users").
- `evidence/project_aliases.json`: a regex for each project and client name, so the storytelling check can see them.
- `evidence/known_errors.json`: start empty; add a rule whenever we catch a mistake.

## Output
Run `python3 scripts/doctor.py`. Summarize what is in the ledger, what is `needs_confirmation`, and the open questions.
Next: `prompts/03_personas_and_resumes.md`.
