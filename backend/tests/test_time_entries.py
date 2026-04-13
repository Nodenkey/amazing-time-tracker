from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_time_entries_returns_seed_data():
    response = client.get("/api/v1/time-entries/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_create_time_entry():
    payload = {
        "date": "2026-04-13",
        "person_name": "Test User",
        "activity": "Writing tests",
        "duration_minutes": 30,
        "notes": "Ensuring API works as expected",
    }
    response = client.post("/api/v1/time-entries/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["person_name"] == "Test User"
    assert body["activity"] == "Writing tests"


def test_get_time_entry_not_found():
    response = client.get("/api/v1/time-entries/non-existent-id")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "not_found"


def test_validation_error_on_blank_person_name():
    payload = {
        "date": "2026-04-13",
        "person_name": " ",
        "activity": "Code review",
        "duration_minutes": 60,
    }
    response = client.post("/api/v1/time-entries/", json=payload)
    assert response.status_code == 422
