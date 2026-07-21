from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import app, main


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 200

    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_the_email():
    client.post("/activities/Chess Club/signup?email=remove-me@mergington.edu")

    response = client.delete(
        "/activities/Chess Club/participants?email=remove-me@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed remove-me@mergington.edu from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert "remove-me@mergington.edu" not in activity["participants"]


def test_main_starts_uvicorn():
    with patch("src.app.uvicorn.run") as mock_run:
        main()

    mock_run.assert_called_once_with(app, host="0.0.0.0", port=8000)
