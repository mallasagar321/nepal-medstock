# Sprint Plans (4 one-week sprints, Scrum)

**Team roles:** Product Owner, Scrum Master, Developer (one person can hold all three in a solo project).

## Sprint 1: Core CRUD API
- **Goal:** health workers can record and update medicine stock.
- **Stories:** US-1, US-2 (6 points)
- **Tasks:** set up repo and Flask skeleton, SQLite schema, POST medicine, PUT stock, unit tests, first CI run
- **Increment:** working add/update API with passing tests

## Sprint 2: Reporting and alerts
- **Goal:** district officers can see stock and spot shortages early.
- **Stories:** US-3, US-4 (8 points)
- **Tasks:** `/stock` endpoint, `/medicines/low-stock` endpoint, tests, Dockerfile, Docker build in CI
- **Increment:** reporting endpoints plus a containerised app

## Sprint 3: Security and polish
- **Goal:** only authorised users change data; app is monitorable and deployable.
- **Stories:** US-5, US-6 (5 points)
- **Tasks:** API key check, `name_ne` field, `/health` endpoint, logging, deploy job, README
- **Increment:** secured, deployed, documented release

## Sprint 4: Web dashboard
- **Goal:** district officers see stock visually, and health workers can update data without Postman.
- **Stories:** US-7, US-8 (8 points)
- **Tasks:** `templates/dashboard.html`, `/dashboard` route, summary cards, low-stock highlighting, add/update forms with API key, dashboard tests, Dockerfile copies `templates/`
- **Increment:** usable web UI on top of the existing API, still tested and deployed by the same pipeline

## Burndown (story points remaining at end of each day)
| Day | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|---|---|---|---|---|
| Start | 6 | 8 | 5 | 8 |
| Day 2 | 5 | 7 | 5 | 7 |
| Day 3 | 4 | 6 | 4 | 5 |
| Day 4 | 3 | 4 | 3 | 3 |
| Day 5 | 1 | 2 | 2 | 1 |
| End | 0 | 0 | 0 | 0 |

*Sample figures: replace with your real numbers when you run the sprints.*
