# Profile & Rules

Last updated: YYYY-MM-DD

Who you are, what you are looking for, and the rules the assistant follows for you. It is filled in during the
setup conversation (`prompts/01_setup_interview.md`) and keeps growing: whenever you state a lasting preference
or correct the assistant, it adds a dated line to the change log at the bottom, in your words.

Numbers that scripts enforce (company limit, duplicate window) also live in `config.json`. Keep them in agreement.

## 1. Basics
- Name:
- Where you live (city, state/country):
- Willing to relocate: (where to, where not, from when)
- Resume contact line: (email | phone | LinkedIn | GitHub or portfolio)
- Education: (school, degree, field, graduation date)
- Current enrollment: (none / details; some programs require current students)

## 2. Work authorization and eligibility
This decides which postings you may apply to. Be exact. The assistant is not a lawyer: questions about your
status go to your school's international office or an immigration attorney, and rules change, so check the
agency's own site (for the U.S., uscis.gov).
- Authorization status: (citizen / permanent resident / visa type and key dates / other)
- Sponsorship needed now: yes / no     Needed in the future: yes / no
- How you answer the standard form questions (authorized to work? will you require sponsorship?):
- Treat as BLOCKED when the posting says: (for example "no sponsorship", citizenship required, active security
  clearance required, "U.S. person" / export-control language)
- Treat as UNKNOWN when: (silence about sponsorship) -> how to verify:
- Other hard blockers: (country, start-date window, graduation or enrollment windows for new-grad programs, degree field)
- Unknown is never eligible: the assistant says "verify first" and names what to check.

## 3. Experience and level
- Professional experience, by function:
- How to count non-job experience when a posting states a minimum (for example "my master's counts as 2 years",
  "internships count as half"). This is a rule for deciding which roles to pursue. Your materials always stay truthful.
- Target level: (what "entry level" means for you; years you treat as met)
- Level stretch means: (for example senior/staff/lead titles, people management, 8+ years)
- Do not want to do again:

## 4. Targets
- Job families in priority order (each becomes a persona and a resume): 1. 2. 3.
- Industries / employer types preferred:
- Industries / employer types to avoid (and why, if you want it remembered):
- Companies to exclude (also in `config.json`): name, reason, date, and an end date if the exclusion expires
- Cities or regions to prioritize: (priority affects ordering, not eligibility, unless you say otherwise)
- Workplace: (onsite / hybrid / remote; countries allowed)
- Salary floor: (and what to do with roles below it: list them, hold them, or send them anyway for interview practice)
- Start-date window: earliest / latest
- Contract, fixed-term and contract-to-hire: acceptable?     Internships: acceptable?
- Target employers (starter list):

## 5. Search rules
- Stretch share of recommended applications: 30%  (skill stretches before level stretches)
- Company limit: 2 applications per company in 60 days  (a planning warning, never a block on recording)
- Posting age limit when sourcing: 30 days  (links you send yourself are triaged regardless of age)
- How often to source: (daily / every 2-3 days / weekly) and which sources
- Applications per week you realistically want to send:
- Send applications the same day they are triaged and tailored? (speed matters: postings fill)
- Optional cover letters: (never / always / only when they add something). The assistant always tells you when a
  posting REQUIRES one.
- Screening questions visible on a form: the assistant drafts answers from your ledger, motives and previous answers.
- Resume length: (one page / two pages)

## 6. Tracking
- Method: (CSV file / Excel workbook / other). Set in `config.json` -> `tracker`.
- Log an application only after you confirm you submitted it. Unknown stays blank.

## 7. Writing and voice
- See `VOICE.md`. Employer rules about AI-assisted applications: the assistant quotes them when a posting states one.
- Edits you make to drafted answers: (a) are true statements the assistant may add to the evidence ledger and reuse
  without asking, or (b) it asks you first. Choose one: ______

## 8. How you finalize resumes
- (For example: take the generated DOCX, compare it with your own formatted master copy, update anything that
  changed, save your copy as PDF, submit the PDF. The assistant never exports PDFs or counts pages for you.)

## 9. Always / never
- Always:
- Never:

## 10. Change log
- YYYY-MM-DD: (rule change, in your words)
