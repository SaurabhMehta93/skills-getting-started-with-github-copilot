from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_contains_chess_club():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_unregister_existing_participant():
    # Ensure the participant exists first
    activities = client.get("/activities").json()
    participants = activities["Chess Club"]["participants"]
    assert "michael@mergington.edu" in participants

    # Delete the participant
    resp = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")
    assert resp.status_code == 200
    assert "Unregistered michael@mergington.edu" in resp.json()["message"]

    # Participant should no longer be present
    activities_after = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities_after["Chess Club"]["participants"]


def test_unregister_nonexistent_participant_returns_400():
    # Try deleting someone not in the list
    resp = client.delete("/activities/Chess%20Club/participants?email=notfound@example.com")
    assert resp.status_code == 400


def test_unregister_nonexistent_activity_returns_404():
    resp = client.delete("/activities/NonExistentActivity/participants?email=test@example.com")
    assert resp.status_code == 404
