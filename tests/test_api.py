
import pytest
from fastapi.testclient import TestClient
from app.main import app, accounts

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_accounts():
    """Réinitialiser les comptes avant chaque test."""
    accounts.clear()
    accounts.update({
        "123": 1000.0,
        "456": 500.0
    })


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to PayFlex API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_balance():
    response = client.get("/accounts/123/balance")
    assert response.status_code == 200
    assert response.json()["balance"] == 1000.0


def test_account_not_found():
    response = client.get("/accounts/999/balance")
    assert response.status_code == 404


def test_successful_payment():
    response = client.post(
        "/payments",
        json={"account_id": "123", "amount": 100}
    )

    assert response.status_code == 200
    assert response.json()["remaining_balance"] == 900.0


def test_insufficient_balance():
    response = client.post(
        "/payments",
        json={"account_id": "123", "amount": 2000}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_payment_unknown_account():
    response = client.post(
        "/payments",
        json={"account_id": "999", "amount": 100}
    )

    assert response.status_code == 404


def test_negative_payment():
    response = client.post(
        "/payments",
        json={"account_id": "123", "amount": -50}
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {"account_id": "123", "amount": None},
        {"account_id": "123", "amount": 0},
        {"amount": 100},
        {"account_id": "123"},
    ],
)
def test_invalid_payment_payloads(payload):
    response = client.post("/payments", json=payload)

    assert response.status_code == 422


def test_payment_amount_as_text():
    response = client.post(
        "/payments",
        json={"account_id": "123", "amount": "not-a-number"}
    )

    assert response.status_code == 422
