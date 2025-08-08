import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime, timezone

# Add the project root to the Python path to allow for absolute imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from schemas import ContactRequestCreate

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
    # Mock the return value from the CRUD function
    mock_db_entry = MagicMock()
    mock_db_entry.id = 1
    mock_db_entry.created_at = datetime.now(timezone.utc)
    # Populate the mock with payload data
    for key, value in valid_payload.items():
        setattr(mock_db_entry, key, value)

    # Patch the functions in the modules where they are looked up
    mock_create_request = mocker.patch("main.crud.create_contact_request", return_value=mock_db_entry)
    mock_send_email = mocker.patch("main.send_contact_email")

    # --- Action ---
    response = client.post("/contact", json=valid_payload)

    # --- Assertions ---
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["name"] == valid_payload["name"]
    assert response_data["email"] == valid_payload["email"]
    assert response_data["id"] == 1
    assert "created_at" in response_data

    # Verify that the mocked functions were called correctly
    mock_create_request.assert_called_once()
    # The `contact_request` argument should be a `ContactRequestCreate` schema instance
    assert isinstance(mock_create_request.call_args.kwargs['contact_request'], ContactRequestCreate)

    mock_send_email.assert_called_once()
    assert isinstance(mock_send_email.call_args.kwargs['contact_request'], ContactRequestCreate)


def test_create_contact_validation_error():
    """
    Test the /contact endpoint with incomplete data to trigger a validation error.
    """
    # --- Action ---
    # Payload is missing the required 'email' and 'service' fields
    invalid_payload = {
        "name": "Test User",
        "message": "This is a test message."
    }
    response = client.post("/contact", json=invalid_payload)

    # --- Assertions ---
    # FastAPI returns a 422 Unprocessable Entity status for validation errors
    assert response.status_code == 422

    response_data = response.json()
    assert "detail" in response_data
    # Check that the error messages mention the missing fields
    errors = {error["loc"][1] for error in response_data["detail"]}
    assert "email" in errors
    assert "service" in errors
