# Sourcing

Sourcing is the assistant's job; checking the result is yours (Checkpoint A). This page lists where it can look and how to add
more.

## Open sources: ready to use

These need no account and are enabled out of the box.

| Source | What it is | How |
|---|---|---|
| **A public listings feed** | A community-maintained JSON feed of new-graduate roles hosted on GitHub. The URL is in `config.json` (`sources.github_feed_url`) and can be replaced with any feed of the same shape. | `python3 scripts/sourcing.py --role-profile <label> --source github --hours 24` |
| **Employers' own job boards** | The public job-board endpoints that Greenhouse and Lever publish for each employer (`boards-api.greenhouse.io`, `api.lever.co`). You list the employers you care about. | `python3 scripts/employer_watch.py --days 2` after adding employers to `employer_watchlist.json` |
| **Links and text you paste** | Anything you found yourself: a referral, an email, a board you browsed. | give the assistant the link or text; or `--source manual --infile postings.txt` |

For every posting kept, the assistant finds it on the **employer's own site**, saves the full text, and confirms title, link, team
and requisition belong together. Aggregator dates and companies are leads, not facts: the employer's page dates the posting.

## Other boards, which may need your account

This repository ships **no scraping scripts** for boards that require an account or restrict automated access (job aggregators,
social networks, school career portals, startup boards). If there are other boards you would like to explore, **ask your
assistant** and follow what it tells you. Expect to:

- **sign in yourself**, in a browser the assistant can see. The assistant must never type your credentials, sign in for you,
  solve a captcha, or like, save, apply, hide or change filters on any site;
- **read and follow each site's terms of service** and any rate limits. Many sites restrict automated access; if a site is not
  open to it, skip the site or use it by hand and paste what you find;
- keep it to **one gentle pass** per source per run, with no repeated paging or retry loops. A site that rate-limits you, shows a
  captcha or signs you out is a stop sign, not a puzzle: report it and move on.

Ask the assistant to list what it read, what it could not read and why, in the sourcing summary.

## Adding a source

Ask the assistant to follow this recipe, and review what it proposes:

1. **Check permission first.** Prefer a documented public API or feed. Read the site's terms and `robots.txt`; if automated
   access is not allowed, stop.
2. **Produce the common shape:** `{title, company, location, url, description, posted}` (see `sourcing.listing_from_feed_row`)
   or the adapter row shape in `employer_watch.py` (`{title, loc, posted, url, id, date_source}`).
3. **Read-only and gentle:** plain GETs, an honest User-Agent, a pause between requests, one request per employer board per run; report a failure and move on.
4. **Add a test** that stubs the network (see `SourcingTests`), and document the source here.
5. **Never store credentials or cookies** in the repository or the workspace.

## Filtering

`config.json` holds the filters: `excluded_companies`, `excluded_keywords`, `excluded_title_patterns` (regexes on the title; a
seniority word at the start of a title excludes it, a mention of senior colleagues does not) and `lane_title_patterns` (feeds
only). The tracker and the skip list are applied automatically; the company limit is checked per posting with
`check_company.py`.

## Freshness

Source at the frequency in your profile and apply the posting-age limit (default 30 days) at sourcing only: links you send the
assistant yourself are triaged whatever their age. A closed or dead posting is still excluded.
