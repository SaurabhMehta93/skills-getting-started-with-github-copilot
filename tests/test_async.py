import pytest


@pytest.mark.asyncio
async def test_root_redirect(async_client):
    resp = await async_client.get("/", allow_redirects=False)
    # RedirectResponse from FastAPI uses 307 by default
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location", "").endswith("/static/index.html")


@pytest.mark.asyncio
async def test_get_activities_contains_programming(async_client):
    resp = await async_client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Programming Class" in data


@pytest.mark.asyncio
async def test_signup_and_unregister_flow(async_client):
    # Sign up a new user
    signup_resp = await async_client.post(
        "/activities/Programming%20Class/signup?email=testuser@example.com"
    )
    assert signup_resp.status_code == 200
    assert "Signed up testuser@example.com for Programming Class" in signup_resp.json()["message"]

    # Confirm present in participants
    activities = (await async_client.get("/activities")).json()
    assert "testuser@example.com" in activities["Programming Class"]["participants"]

    # Unregister the user
    del_resp = await async_client.delete(
        "/activities/Programming%20Class/participants?email=testuser@example.com"
    )
    assert del_resp.status_code == 200
    assert "Unregistered testuser@example.com" in del_resp.json()["message"]

    # Ensure removed
    activities_after = (await async_client.get("/activities")).json()
    assert "testuser@example.com" not in activities_after["Programming Class"]["participants"]


@pytest.mark.asyncio
async def test_signup_existing_participant_returns_400(async_client):
    # 'emma@mergington.edu' is already in Programming Class
    resp = await async_client.post(
        "/activities/Programming%20Class/signup?email=emma@mergington.edu"
    )
    assert resp.status_code == 400
