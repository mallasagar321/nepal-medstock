# Sprint Reviews and Retrospectives

## Sprint 1
**Review (demo):** added a health post and a medicine, updated stock, showed rejected invalid input.
**Went well:** small scope, tests written alongside code, CI caught a lint error early.
**To improve:** validation rules were unclear at the start; define acceptance criteria during planning.
**Action:** write acceptance criteria for every story before the sprint starts.

## Sprint 2
**Review (demo):** `/stock` overview and low-stock list; Docker image running locally.
**Went well:** acceptance criteria made testing easy; Docker gave the same behaviour everywhere.
**To improve:** no way to restrict who edits data yet.
**Action:** prioritise security in Sprint 3.

## Sprint 3
**Review (demo):** 401 without API key, Nepali medicine names, `/health` check, auto-deploy from `main`.
**Went well:** full pipeline (test, build, deploy) ran without manual steps.
**To improve:** SQLite resets on free hosting; plan PostgreSQL next.
**Action:** add PostgreSQL and SMS alerts to the future backlog.

## Sprint 4
**Review (demo):** opened `/dashboard`, showed red LOW rows, added a medicine and changed a quantity from the browser.
**Went well:** the existing API and tests made the UI quick to build; the same CI pipeline covered the new page.
**To improve:** the dashboard uses a shared API key field, not real user accounts.
**Action:** add proper login (per-user accounts) to the future backlog.

*These are sample entries: edit them to match what actually happened in your sprints.*
