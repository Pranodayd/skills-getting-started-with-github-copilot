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


def test_main_starts_uvicorn():
    with patch("src.app.uvicorn.run") as mock_run:
        main()

    mock_run.assert_called_once_with(app, host="0.0.0.0", port=8000)
