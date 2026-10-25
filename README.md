# Nepal Health Post Medicine Stock Tracker

**Problem:** Many remote health posts in Nepal run out of essential medicines because stock is tracked
on paper and the district office finds out too late.
**Solution:** A small REST API where health posts record stock and district officers see what is low.

Built with **Agile (Scrum)** for planning and **DevOps (Git, CI/CD, Docker)** for delivery.
See the `docs/` folder for the backlog, sprint plans, stand-up log, retrospectives and pipeline.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
API_KEY=my-secret python app.py                       # Windows: set API_KEY=my-secret
```
The API runs at http://localhost:5000 and the web dashboard at http://localhost:5000/dashboard

## Run tests and lint
```bash
pytest -v
flake8 .
```

## Run with Docker
```bash
docker compose up --build
```

## API
Write endpoints need the header `X-API-Key: <your key>` (default `dev-key`). Reads are public.

| Method | Endpoint | Purpose | Sprint |
|---|---|---|---|
| GET | `/` | Project name and endpoint list | 4 |
| GET | `/dashboard` | Web dashboard: stock table, low-stock highlights, forms | 4 |
| GET | `/health` | Monitoring check | 3 |
| POST | `/posts` | Add a health post `{name, district}` | 1 |
| POST | `/posts/<id>/medicines` | Add medicine `{name, name_ne?, quantity, threshold?}` | 1 |
| PUT | `/medicines/<id>` | Update stock with `{quantity}` or `{dispensed}` | 1 |
| GET | `/stock` | All posts and their stock | 2 |
| GET | `/medicines/low-stock` | Medicines below threshold | 2 |

### Try it (curl)
```bash
curl -X POST localhost:5000/posts -H "X-API-Key: dev-key" -H "Content-Type: application/json" \
     -d '{"name":"Jumla Health Post","district":"Jumla"}'
curl -X POST localhost:5000/posts/1/medicines -H "X-API-Key: dev-key" -H "Content-Type: application/json" \
     -d '{"name":"ORS","name_ne":"जीवनजल","quantity":10,"threshold":20}'
curl localhost:5000/medicines/low-stock
```
(Windows CMD users: use Postman instead of curl quoting.)

## Git workflow
```bash
git init && git add . && git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
Then work on feature branches (`feature/low-stock`), open pull requests, and let GitHub Actions run.

## Deploy (optional)
Create a Web Service on Render from the GitHub repo (Docker runtime), set `API_KEY`, copy its Deploy Hook
URL into the GitHub secret `RENDER_DEPLOY_HOOK`. Every push to `main` that passes CI then redeploys.
Note: free tiers have ephemeral disks, so SQLite data resets on redeploy; this is fine for a demo.

## Future scope
SMS alerts for low stock, offline-first mobile entry for poor connectivity, PostgreSQL, full Nepali UI.
