import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timezone

# Add the project root to the Python path to allow for absolute imports
# This is necessary because the tests are in a subfolder of the package
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from backend.main import app
from backend.schemas import ContactRequestCreate

client = TestClient(app)

@pytest.fixture
def valid_payload():
    """Provides a valid contact request payload for tests."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "service": "Testing Service",
        "message": "This is a test message."
    }

def test_create_contact_success(mocker, valid_payload):
    """
    Test a successful submission to the /contact endpoint.
    """
    # --- Mocking ---
    mock_db_entry = MagicMock()
    mock_db_entry.id = 1
    mock_db_entry.created_at = datetime.now(timezone.utc)
    for key, value in valid_payload.items():
        setattr(mock_db_entry, key, value)

    # Patch the functions where they are looked up
    mock_create_request = mocker.patch("backend.main.crud.create_contact_request", return_value=mock_db_entry)
    mock_send_email = mocker.patch("backend.main.send_contact_email")

    # --- Action ---
    response = client.post("/contact", json=valid_payload)

    # --- Assertions ---
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["name"] == valid_payload["name"]
    assert "id" in response_data

    mock_create_request.assert_called_once()
    assert isinstance(mock_create_request.call_args.kwargs['contact_request'], ContactRequestCreate)

    mock_send_email.assert_called_once()
    assert isinstance(mock_send_email.call_args.kwargs['contact_request'], ContactRequestCreate)


def test_create_contact_validation_error():
    """
    Test the /contact endpoint with incomplete data to trigger a validation error.
    """
    invalid_payload = { "name": "Test User", "message": "Missing email" }
    response = client.post("/contact", json=invalid_payload)
    assert response.status_code == 422

    response_data = response.json()
    assert "detail" in response_data
    errors = {error["loc"][1] for error in response_data["detail"]}
    assert "email" in errors
    assert "service" in errors
