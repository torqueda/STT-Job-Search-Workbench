# Tests

```bash
python3 -m unittest discover -s tests -v      # or: make test
```

77 tests, no live network calls. Runtime depends on your Python environment. Tests use temporary files and throw-away copies of the **fictional** demo workspace
(`examples/demo_persona/workspace`), so tests never read or write real data. Network calls (employer boards, the listings feed)
are stubbed.

## What each group protects

**EvidenceResolutionTests (11)** - resumes come only from registered claims.
A legacy spec cannot regenerate; a batch cannot replace persona content; reordering keeps required claims; a persona that loses a
required claim is blocked; stale revision and family mismatch fail; a label cannot overwrite another persona; every active persona
resolves cleanly; a retired persona is refused; every project carries a registered purpose line; an unregistered purpose and a
claim that is not `usable` are blocked.

**ContentCheckTests (7)** - known errors, editorial warnings, and review binding.
Known-error rules block unsupported claims; an `unless` clause lets qualified wording through; editorial warnings fire, need a
recorded resolution, and can be disabled in config; a review is bound to normalized extracted text and to the ledger revision; a review may cite
reflections but not unknown IDs.

**StorytellingTests (8)** - the storytelling check.
A project named without its kind or purpose is flagged; an introduced project passes; stock motive phrases are flagged and a
first-person motive is not; with no aliases registered the project check is inactive; a writing review needs every storytelling flag
resolved while a resume does not; answer extraction reads blockquotes first, then long paragraphs; the demo's two answers come out
clean and flagged.

**TrackerTests (16)** - the tracker and the report.
URL normalization keeps requisition identifiers and drops tracking parameters; CSV round trip makes a backup before writing; backups
are pruned to the configured count; a second writer is refused while a lock exists; the Excel backend preserves unrelated cells and
dates; a new application needs confirmation and an evidence trail; the resume spec must name the company; duplicate URL and
requisition are fatal but the company cap only warns; incomplete attempts do not count; a stage change needs a date while a rejection
defaults to today; a dry run changes nothing; an update keeps identity fields; cohorts never call a blank outcome a rejection;
the company cap and an expiring exclusion behave correctly; the exclusion end date is inclusive and honors
`--as-of`; submission dates cannot be assumed.

**SourcingTests (11)** - filters and sources.
A junior posting is not dropped for mentioning senior colleagues; reasons for dropping are counted separately; lane patterns apply
to feeds only; feed rows are filtered by activity and age; manual blocks parse; repeat batches preserve earlier content, and batch labels cannot escape the output folder; the employer watcher reads Greenhouse and Lever, applies level, location, age and lane filters, reports manual
employers, and keeps going when one employer errors. Failed board requests are made once, excluded employers are not fetched,
and expired exclusions do not remove feed listings.

**PackageAndDocumentTests (11)** - documents and packages.
A package preserves files and detects later edits; it refuses without Gate 1 approval or with a stale review; the resume document
contains the registered purpose line and the generator respects the Gate 1 flag; a legacy spec fails in the generator; content limits
warn without blocking; letter checks flag padding phrases and configured opening/closing sentences; output filenames strip unsafe
characters. Existing resume outputs are preserved, unregistered experience bullets block generation, package paths
resolve relative to the workspace, and packaging honors the configured resume page limit.

**WorkspaceAndHygieneTests (13)** - setup and release hygiene.
`init_workspace` copies templates and never overwrites; a fresh workspace is valid but warns about what is empty; `doctor` is clean on
the demo and catches broken references, invalid regexes, unusable claims and resume lines that are not ledger claims; the skip list is
append-only and deduplicated; `archive_handoff` moves only older entries; `pii_scan` flags emails, phone numbers, SSNs, home paths,
keys, LinkedIn profiles and deny-list terms while allowing placeholders; the repository itself passes the scan; **demo documents are
labelled FICTIONAL** and workspace scripts announce the demo workspace. Configuration and metro regexes are checked; filenames are
scanned, and symlinks and binary files are flagged for manual inspection.

## Adding a test

Subclass `DemoWorkspaceCase` (it gives each test its own copy of the demo workspace and helpers such as `review()`). Stub the network.
If you add a script, add a test for its refusals (what it must not do), not only for its happy path.
