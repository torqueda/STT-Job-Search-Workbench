# Publishing safely

For anyone publishing a fork or an updated copy of this repository (or anything derived from a personal workspace).

1. **Never publish a workspace.** `/workspace/` is ignored by git. Work in a fresh clone or a fresh folder, not in a folder that has
   held your real files, so personal data never enters history. Deleting a file does not remove it from earlier commits. If personal data was committed, clean the history before
   publishing; if a credential was exposed, revoke it. This scanner does not inspect history.
2. **Write a deny-list outside the repository:** your name variants, email, phone, address, employers, schools, project and client
   names, numbers from your resume, one per line (`re:` prefix for a regex). Keep it out of the repo (the `.gitignore` also ignores
   `denylist*.txt` as a last resort).
3. **Scan:** `python3 scripts/pii_scan.py --root . --denylist ~/private/denylist.txt [--allow LICENSE:Name]`. Resolve every finding.
   Allow your name only where you intend attribution, such as the MIT copyright notice.
   The built-in scan cannot detect arbitrary names, schools, employers or distinctive personal narratives.
4. **Read the file list and the diff yourself.** Use `git ls-files` and `git diff --check` when Git metadata is available.
   Check ignored files too if distributing an archive: ZIP tools can include `workspace/` regardless of Git rules.
   The scan skips the top-level private workspace and tool caches; it is a release-source scan, not a privacy audit of those folders. A clean scan is evidence, not proof. Binary files (PDF, DOCX, images) are reported
   as not scanned: inspect or remove them.
5. **Run the tests:** `make test`. The suite includes a check that every demo file is labelled FICTIONAL and that the repository
   passes the built-in scan.
6. **Check the examples** still use only invented names, `example.com` addresses and the reserved fictional phone range.
7. **Say what you did not test.** Keep [LLM_COMPATIBILITY.md](LLM_COMPATIBILITY.md) honest about the assistants you have used.

## Scope of the privacy check

The scan checks UTF-8 source text and filenames for common contact, identifier, home-path and credential patterns, plus
any terms in your private deny-list. Binary files and symlinks are flagged for inspection. A clean result does not prove
anonymity, detect every kind of secret, or inspect document metadata or deleted files. Scan the exact folder you intend
to distribute, and review its contents yourself.

An ignored workspace is still readable by your assistant. Review the assistant provider's retention and data-use
settings before giving it personal or confidential files. Use invented fixtures for tests, screenshots and portfolio demos.
