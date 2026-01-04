import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    email = "test_user_1@example.com"
    password = "password123"

    response = await client.post(
        "/users/",
        json={"email": email, "password": password}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    email = "duplicate@example.com"
    password = "password123"

    response_1 = await client.post(
        "/users/",
        json={"email": email, "password": password}
    )
    assert response_1.status_code == 201

    response_2 = await client.post(
        "/users/",
        json={"email": email, "password": password}
    )

    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "User with this email already exists"