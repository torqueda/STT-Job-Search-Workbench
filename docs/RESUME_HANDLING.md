# From generated DOCX to the file you submit

The generator produces an **editable DOCX per persona**, with a compact layout intended for a short resume. It is a draft assembled from your ledger, not the file you send.
How you turn it into the final document is up to you. The assistant does not export PDFs or count pages for you: layout depends on
your fonts and software, and the page count of the file you actually send is the one that matters.

## One way to finalize a resume (which is also my personal approach)

1. The assistant identifies the persona each role uses and generates the DOCX files in `workspace/tailored_resumes/`.
2. Keep a **formatted master copy** of each persona's resume in your private workspace. Compare the generated file
   with that copy and update it for anything that changed (a new claim, a reordered project, a corrected line).
3. Export the final copy as a PDF, check the page count and layout, and submit it yourself.
4. If a wording edit adds a true statement the ledger lacks, tell the assistant so it can record it (see [PERSONALIZING.md](PERSONALIZING.md)).

Other reasonable approaches: submit the generated DOCX after your own formatting pass; paste the text into a template you like;
or let the generated file be only a checklist of what each persona must say.

## Practical notes

- **Review the file you send, not the file the assistant made.** A review is tied to normalized extracted text; wording edits make it stale. Inspect formatting changes yourself.
  If you use `application_package.py`, record the final file, its page count and how you inspected it.
- **Quick Look and other previews are approximate.** Right-aligned dates and fonts can differ from Word.
- **Parsers are literal.** An applicant-tracking system can attach a section to the wrong job if a heading is unusual. The section
  labels are configurable in `base_resume.json` (`style.projects_heading`, `style.experience_heading`); if a form's parsed resume
  looks wrong, change the label rather than the content.
- **Name files the way the employer expects** ("First Last - Resume.pdf"). Keep submitted copies in a folder of your own, inside
  your private workspace or an external private folder.
- **Never publish exported PDFs.** They are personal documents. The default workspace is ignored by Git.
- **Page limits are configurable.** Set `config.json` -> `resume_limits.max_pages` to match your profile (default 1).
  Generation does not measure pages; packaging checks the page count you record in the review.
