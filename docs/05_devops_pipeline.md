# DevOps Pipeline

```
Developer -> git push / pull request
          -> GitHub Actions: install -> flake8 -> pytest
          -> Docker build
          -> Deploy hook (Render) on main
          -> Monitor: /health endpoint + logs
```

| Stage | Tool | File |
|---|---|---|
| Plan | GitHub Projects board (To Do / In Progress / Done) | n/a |
| Code | Git, feature branches, pull requests | n/a |
| Build and test | GitHub Actions, flake8, pytest | `.github/workflows/ci.yml` |
| Package | Docker (copies `app.py` and `templates/`) | `Dockerfile`, `docker-compose.yml` |
| Release | Render deploy hook, triggered only if tests pass | `ci.yml` (deploy job) |
| Monitor | `/health` endpoint, Docker HEALTHCHECK, app logs | `app.py` |

## How Agile and DevOps connect
Agile decides what to build and when (backlog, sprints, reviews). DevOps makes sure each sprint's code is
tested, packaged and released automatically, so every sprint ends with a working, deployed increment.
