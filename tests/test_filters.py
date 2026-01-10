import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_search_and_pagination(
        client: AsyncClient,
        normal_user_token_headers: dict
):
    """
    Test filtering by keyword and pagination limits.
    """
    events_payloads = [
        {
            "title": "Python Workshop",
            "description": "Learn python basics",
            "date_time": "2026-05-20T10:00:00",
            "slots": 10
        },
        {
            "title": "Docker Masterclass",
            "description": "Containers deep dive",
            "date_time": "2026-05-21T10:00:00",
            "slots": 5
        },
        {
            "title": "Summer Music Festival",
            "description": "Fun and music",
            "date_time": "2026-06-01T18:00:00",
            "slots": 100
        },
    ]

    for payload in events_payloads:
        res = await client.post("/events/", json=payload, headers=normal_user_token_headers)
        assert res.status_code == 201

    response = await client.get("/events/?keyword=Docker", headers=normal_user_token_headers)
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Docker Masterclass"

    response = await client.get("/events/?limit=2", headers=normal_user_token_headers)
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

    response = await client.get("/events/?skip=1&limit=2", headers=normal_user_token_headers)
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] != "Python Workshop"
