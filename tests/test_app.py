from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.app import app, main


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_duplicate_signup_is_rejected(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    first_response = client.post(f"/activities/Chess Club/signup?email={email}")
    second_response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_the_email(client):
    # Arrange
    email = "remove-me@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")

    # Act
    response = client.delete(f"/activities/Chess Club/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert email not in activity["participants"]


def test_main_starts_uvicorn():
    # Arrange
    with patch("src.app.uvicorn.run") as mock_run:
        # Act
        main()

    # Assert
    mock_run.assert_called_once_with(app, host="0.0.0.0", port=8000)
