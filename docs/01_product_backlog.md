# Product Backlog

| ID | User story | Priority | Points | Sprint | Status |
|---|---|---|---|---|---|
| US-1 | As a health worker, I can add a medicine with its quantity, so stock is recorded. | High | 3 | 1 | Done |
| US-2 | As a health worker, I can update stock after dispensing. | High | 3 | 1 | Done |
| US-3 | As a district officer, I can view all health posts and their stock. | High | 3 | 2 | Done |
| US-4 | As a district officer, I get a low-stock list (quantity below a threshold). | High | 5 | 2 | Done |
| US-5 | As an admin, I can log in so only authorised users edit data (API key). | Medium | 3 | 3 | Done |
| US-6 | As a user, I can see medicine names in Nepali (`name_ne` field; full Nepali UI is future work). | Low | 2 | 3 | Done (partial) |
| US-7 | As a district officer, I can see all stock on a web dashboard with low-stock items highlighted in red. | High | 5 | 4 | Done |
| US-8 | As a health worker, I can add posts and medicines and update stock from the dashboard. | Medium | 3 | 4 | Done |

## Definition of Done
- Code reviewed through a pull request
- Unit tests written and passing in CI
- Lint (flake8) clean
- Docker image builds
- Demoed in the sprint review

## Acceptance criteria (examples)
- **US-2:** dispensing more than available stock is rejected with HTTP 400.
- **US-4:** only medicines with `quantity < threshold` appear, lowest stock first.
- **US-7:** `/dashboard` loads, shows totals, and rows below threshold are red with a LOW badge.
- **US-5:** POST/PUT without a valid `X-API-Key` return HTTP 401.
