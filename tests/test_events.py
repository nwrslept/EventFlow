import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_event(authorized_client: AsyncClient):
    response = await authorized_client.post(
        "/events/",
        json={
            "title": "Test Party",
            "description": "Fun time",
            "location": "Kyiv",
            "date_time": "2030-01-01T12:00:00"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Party"
    assert "id" in data
    assert "owner_id" in data


@pytest.mark.asyncio
async def test_read_events(authorized_client: AsyncClient):
    await authorized_client.post(
        "/events/",
        json={"title": "Event 1", "date_time": "2030-01-01T10:00:00"}
    )

    response = await authorized_client.get("/events/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == "Event 1"


@pytest.mark.asyncio
async def test_update_event(authorized_client: AsyncClient):
    res_create = await authorized_client.post(
        "/events/",
        json={"title": "Old Title", "date_time": "2030-01-01T10:00:00"}
    )
    event_id = res_create.json()["id"]

    res_update = await authorized_client.put(
        f"/events/{event_id}",
        json={"title": "New Title", "date_time": "2030-01-01T10:00:00"}
    )
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_event(authorized_client: AsyncClient):
    res_create = await authorized_client.post(
        "/events/",
        json={"title": "To Delete", "date_time": "2030-01-01T10:00:00"}
    )
    event_id = res_create.json()["id"]

    res_delete = await authorized_client.delete(f"/events/{event_id}")
    assert res_delete.status_code == 204

    res_get = await authorized_client.get(f"/events/{event_id}")
    assert res_get.status_code == 404


@pytest.mark.asyncio
async def test_delete_event_unauthorized(authorized_client: AsyncClient):

    res = await authorized_client.post(
        "/events/",
        json={"title": "Secret Event", "date_time": "2030-01-01T10:00:00"}
    )
    assert res.status_code == 201
    event_id = res.json()["id"]

    del authorized_client.headers["Authorization"]

    res_fail = await authorized_client.delete(f"/events/{event_id}")
    assert res_fail.status_code == 401


@pytest.mark.asyncio
async def test_search_events(authorized_client: AsyncClient):
    await authorized_client.post(
        "/events/",
        json={"title": "Rock Concert", "description": "Loud music", "date_time": "2030-01-01T19:00:00"}
    )

    await authorized_client.post(
        "/events/",
        json={"title": "Football Match", "description": "Champions league", "date_time": "2030-01-02T19:00:00"}
    )

    res_search = await authorized_client.get("/events/?keyword=Concert")
    assert res_search.status_code == 200
    data = res_search.json()

    assert len(data) == 1
    assert data[0]["title"] == "Rock Concert"

    res_desc = await authorized_client.get("/events/?keyword=league")
    assert len(res_desc.json()) == 1
    assert res_desc.json()[0]["title"] == "Football Match"