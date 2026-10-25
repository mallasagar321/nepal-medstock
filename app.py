import os
import sqlite3
import logging
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, g, jsonify, render_template, request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("medstock")

SCHEMA = """
CREATE TABLE IF NOT EXISTS health_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    district TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL REFERENCES health_posts(id),
    name TEXT NOT NULL,
    name_ne TEXT,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    threshold INTEGER NOT NULL DEFAULT 20,
    updated_at TEXT NOT NULL
);
"""


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_app(db_path=None, api_key=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get("DB_PATH", "medstock.db")
    app.config["API_KEY"] = api_key or os.environ.get("API_KEY", "dev-key")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DB_PATH"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        get_db().executescript(SCHEMA)

    def require_key(fn):
        """Sprint 3 (US-5): only authorised users may change data."""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.headers.get("X-API-Key") != app.config["API_KEY"]:
                return jsonify(error="unauthorised"), 401
            return fn(*args, **kwargs)
        return wrapper

    # ---- Home and dashboard (Sprint 4: US-7) --------------------------
    @app.get("/")
    def home():
        return jsonify(
            name="Nepal Health Post Medicine Stock Tracker",
            endpoints=["/dashboard", "/health", "/stock", "/medicines/low-stock"],
        )

    @app.get("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    # ---- Monitoring -------------------------------------------------
    @app.get("/health")
    def health():
        get_db().execute("SELECT 1")
        return jsonify(status="ok", time=now())

    # ---- Health posts -----------------------------------------------
    @app.post("/posts")
    @require_key
    def add_post():
        data = request.get_json(silent=True) or {}
        if not data.get("name") or not data.get("district"):
            return jsonify(error="name and district are required"), 400
        db = get_db()
        cur = db.execute("INSERT INTO health_posts (name, district) VALUES (?, ?)",
                         (data["name"], data["district"]))
        db.commit()
        log.info("health post %s created", cur.lastrowid)
        return jsonify(id=cur.lastrowid, name=data["name"], district=data["district"]), 201

    # ---- Sprint 1: US-1 add medicine --------------------------------
    @app.post("/posts/<int:post_id>/medicines")
    @require_key
    def add_medicine(post_id):
        db = get_db()
        if not db.execute("SELECT 1 FROM health_posts WHERE id=?", (post_id,)).fetchone():
            return jsonify(error="health post not found"), 404
        data = request.get_json(silent=True) or {}
        qty = data.get("quantity")
        if not data.get("name") or not isinstance(qty, int) or qty < 0:
            return jsonify(error="name and a non-negative integer quantity are required"), 400
        cur = db.execute(
            "INSERT INTO medicines (post_id, name, name_ne, quantity, threshold, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (post_id, data["name"], data.get("name_ne"), qty, data.get("threshold", 20), now()))
        db.commit()
        return jsonify(id=cur.lastrowid), 201

    # ---- Sprint 1: US-2 update stock --------------------------------
    @app.put("/medicines/<int:med_id>")
    @require_key
    def update_stock(med_id):
        db = get_db()
        row = db.execute("SELECT * FROM medicines WHERE id=?", (med_id,)).fetchone()
        if not row:
            return jsonify(error="medicine not found"), 404
        data = request.get_json(silent=True) or {}
        if "quantity" in data:
            new_qty = data["quantity"]
        elif "dispensed" in data:
            new_qty = row["quantity"] - data["dispensed"]
        else:
            return jsonify(error="send 'quantity' or 'dispensed'"), 400
        if not isinstance(new_qty, int) or new_qty < 0:
            return jsonify(error="resulting quantity must be a non-negative integer"), 400
        db.execute("UPDATE medicines SET quantity=?, updated_at=? WHERE id=?",
                   (new_qty, now(), med_id))
        db.commit()
        return jsonify(id=med_id, quantity=new_qty)

    # ---- Sprint 2: US-3 view all stock ------------------------------
    @app.get("/stock")
    def all_stock():
        rows = get_db().execute(
            "SELECT p.id AS post_id, p.name AS post, p.district, m.id AS medicine_id, "
            "m.name, m.name_ne, m.quantity, m.threshold, m.updated_at "
            "FROM health_posts p LEFT JOIN medicines m ON m.post_id = p.id "
            "ORDER BY p.district, p.name, m.name").fetchall()
        return jsonify([dict(r) for r in rows])

    # ---- Sprint 2: US-4 low-stock alerts ----------------------------
    @app.get("/medicines/low-stock")
    def low_stock():
        rows = get_db().execute(
            "SELECT p.name AS post, p.district, m.id AS medicine_id, m.name, m.name_ne, "
            "m.quantity, m.threshold FROM medicines m JOIN health_posts p ON p.id = m.post_id "
            "WHERE m.quantity < m.threshold ORDER BY m.quantity ASC").fetchall()
        return jsonify([dict(r) for r in rows])

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
