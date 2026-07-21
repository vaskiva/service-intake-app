import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


client = TestClient(app)


VALID_REQUEST = {
    "language": "en",
    "category": "plumbing",
    "description": "Water is leaking under the kitchen sink.",
    "postal_code": "10300",
    "customer_name": "Tiina Smith",
    "email": "tiina@example.com",
}


@pytest.fixture(autouse=True)
def reset_storage() -> None:
    """Reset in-memory storage before every test."""
    storage._requests.clear()
    storage._next_id = 1


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_service_request() -> None:
    response = client.post(
        "/requests",
        json=VALID_REQUEST,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "received"
    assert data["language"] == "en"
    assert data["category"] == "plumbing"
    assert data["email"] == "tiina@example.com"


def test_reject_invalid_service_request() -> None:
    invalid_request = {
        **VALID_REQUEST,
        "email": "not-an-email",
    }

    response = client.post(
        "/requests",
        json=invalid_request,
    )

    assert response.status_code == 422


def test_list_service_requests() -> None:
    client.post(
        "/requests",
        json=VALID_REQUEST,
    )

    second_request = {
        **VALID_REQUEST,
        "category": "electrical",
        "description": "The kitchen ceiling light no longer turns on.",
        "email": "daniel@example.com",
    }

    client.post(
        "/requests",
        json=second_request,
    )

    response = client.get("/requests")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


def test_get_service_request_by_id() -> None:
    create_response = client.post(
        "/requests",
        json=VALID_REQUEST,
    )

    request_id = create_response.json()["id"]

    response = client.get(f"/requests/{request_id}")

    assert response.status_code == 200
    assert response.json()["id"] == request_id
    assert response.json()["email"] == "tiina@example.com"


def test_get_missing_service_request() -> None:
    response = client.get("/requests/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Service request not found"
    }

def test_update_service_request_status() -> None:
    response = client.post(
        "/requests",
        json=VALID_REQUEST,
    )

    request_id = response.json()["id"]

    response = client.patch(
        f"/requests/{request_id}/status",
        json={"status": "accepted"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == request_id
    assert response.json()["status"] == "accepted"

    get_response = client.get(f"/requests/{request_id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "accepted"


def test_update_missing_service_request() -> None:
    response = client.patch(
        "/requests/999/status",
        json={"status": "accepted"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Service request not found"
    }

def test_reject_invalid_request_status() -> None:
    create_response = client.post(
        "/requests",
        json=VALID_REQUEST,
    )

    request_id = create_response.json()["id"]

    response = client.patch(
        f"/requests/{request_id}/status",
        json={"status": "something_random"},
    )

    assert response.status_code == 422