import pytest
from app import create_app

KEY = {"X-API-Key": "test-key"}


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=str(tmp_path / "test.db"), api_key="test-key")
    return app.test_client()


def make_post(client):
    return client.post("/posts", json={"name": "Jumla Health Post", "district": "Jumla"},
                       headers=KEY).get_json()["id"]


def make_med(client, post_id, qty=100, threshold=20, name="Paracetamol"):
    return client.post(f"/posts/{post_id}/medicines",
                       json={"name": name, "name_ne": "प्यारासिटामोल", "quantity": qty,
                             "threshold": threshold},
                       headers=KEY).get_json()["id"]


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"


# Sprint 1
def test_add_medicine(client):
    pid = make_post(client)
    r = client.post(f"/posts/{pid}/medicines", json={"name": "ORS", "quantity": 50}, headers=KEY)
    assert r.status_code == 201


def test_add_medicine_validation(client):
    pid = make_post(client)
    r = client.post(f"/posts/{pid}/medicines", json={"name": "ORS", "quantity": -5}, headers=KEY)
    assert r.status_code == 400


def test_add_medicine_unknown_post(client):
    r = client.post("/posts/99/medicines", json={"name": "ORS", "quantity": 5}, headers=KEY)
    assert r.status_code == 404


def test_update_quantity_and_dispense(client):
    mid = make_med(client, make_post(client), qty=100)
    assert client.put(f"/medicines/{mid}", json={"quantity": 80}, headers=KEY).get_json()["quantity"] == 80
    assert client.put(f"/medicines/{mid}", json={"dispensed": 30}, headers=KEY).get_json()["quantity"] == 50


def test_cannot_dispense_more_than_stock(client):
    mid = make_med(client, make_post(client), qty=10)
    assert client.put(f"/medicines/{mid}", json={"dispensed": 11}, headers=KEY).status_code == 400


# Sprint 2
def test_all_stock(client):
    pid = make_post(client)
    make_med(client, pid)
    data = client.get("/stock").get_json()
    assert len(data) == 1 and data[0]["district"] == "Jumla"


def test_low_stock_list(client):
    pid = make_post(client)
    make_med(client, pid, qty=5, threshold=20, name="Amoxicillin")
    make_med(client, pid, qty=500, threshold=20, name="Paracetamol")
    low = client.get("/medicines/low-stock").get_json()
    assert [m["name"] for m in low] == ["Amoxicillin"]


# Sprint 3
def test_write_requires_api_key(client):
    r = client.post("/posts", json={"name": "X", "district": "Y"})
    assert r.status_code == 401


def test_read_is_public(client):
    assert client.get("/stock").status_code == 200


# Sprint 4 (US-7): dashboard
def test_dashboard_page(client):
    r = client.get("/dashboard")
    assert r.status_code == 200
    assert b"Medicine Stock Dashboard" in r.data


def test_home_lists_dashboard(client):
    assert "/dashboard" in client.get("/").get_json()["endpoints"]
