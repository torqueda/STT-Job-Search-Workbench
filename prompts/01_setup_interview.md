# 01 - Initial setup interview

Use once, in the first session, after `python3 scripts/init_workspace.py` has created your workspace. Open your
assistant in this repository folder and say: **"Read AGENTS.md, then run prompts/01_setup_interview.md."**

You do not need perfect answers. The rules grow with use: industries you never want, a consistent tone, and
exclusions usually appear in the first few weeks. Capture what you know now; the assistant records every later
correction in `PROFILE_AND_RULES.md` and `VOICE.md`.

---

Interview me to fill in my workspace. Work **one section at a time**, wait for my answers, keep each message short,
and give examples of the kind of answer you need. If I say "I don't know", write "unknown - to check" and list it as
a to-do. Never give legal or immigration advice; record my facts and flag questions for the right professional.

## Step 1 - Material to collect
Ask me for, and read, the following (any of it can be missing; say what is missing and carry on):
- **My current resume** (any format). I may ask you for honest feedback on it; give it, separately from the setup.
- **Experience beyond the resume:** portfolio or GitHub links, course projects, capstones, research, volunteering,
  previous work, certifications, languages, anything I am proud of.
- **Writing samples:** cover letters, essays, application answers, or messages I wrote. For each, ask who actually
  wrote it (me, an AI tool, or both). Only what I wrote myself is a voice reference. If I have none, a few paragraphs
  typed right here in the chat will do.

## Step 2 - Profile and rules (`PROFILE_AND_RULES.md`, `config.json`)
Walk through the sections of `PROFILE_AND_RULES.md` in order and fill each in:
1. **Basics:** name, location, relocation, contact line, education, current enrollment.
2. **Work authorization and eligibility:** my exact situation; what posting language blocks me; what counts as unknown
   and how to verify it; start-date, graduation-window and enrollment blockers.
3. **Experience and level:** how I want non-job experience counted when a posting states years (rule for choosing
   roles only; materials stay truthful); what "level stretch" means for me.
4. **Targets (the musts and must-nots):** job families in priority order; industries and companies to avoid, with
   reasons; cities or regions to prioritize; workplace and country limits; salary floor and what to do with roles
   below it; start window; contract and internship stance; target employers.
5. **Search rules:** stretch share (default 30%), company limit (default 2 per 60 days), posting-age limit (default
   30 days), how often to source and from where, applications per week, same-day sending, cover-letter preference
   (never / always / only when they add something; you always tell me when one is required), resume length.
6. **Tracking:** how I want to track applications (CSV, Excel, other) and where the file lives.
7. **Writing and voice:** employer rules about AI-assisted applications; whether my edits to your drafts may be added
   to my evidence ledger without asking (they are statements I wrote about my own experience).
8. **How I finalize resumes:** for example "I take your DOCX, compare it with my own formatted copy kept elsewhere,
   update anything that changed, save my copy as PDF and submit that". You never export PDFs or count pages for me.
9. **Always / never** lists, and anything else I would want a different job seeker to be asked as well. Suggest
   questions I have not thought of (for example internships, remote preference, pay-transparency, school-specific
   rules, referral contacts to ask before applying).

Write each answer into the file in my own words, and write the numbers the scripts use into `config.json`
(`tracker`, `duplicate_check_days_threshold`, `max_applications_per_company_in_window`, `excluded_companies`,
`excluded_title_patterns`, `resume_limits.max_pages`).

## Step 3 - Voice (`VOICE.md`)
From the samples I gave, describe how I write in a few lines; list each sample with who wrote it; add my stated
preferences. Do not copy phrases from AI-written samples into the voice section.

## Step 4 - Next
Tell me what is still unknown, then the next steps: build the evidence ledger (`prompts/02_evidence_builder.md`),
then personas and resumes (`prompts/03_personas_and_resumes.md`). Add a `HANDOFF.md` entry for this session and run
`python3 scripts/doctor.py`.
