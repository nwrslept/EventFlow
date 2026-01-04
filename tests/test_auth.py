import pytest
from httpx import AsyncClient
from app.core.security import get_password_hash
from app.models.user import User


async def create_dummy_user(session, email, password):
    user = User(email=email, hashed_password=get_password_hash(password))
    session.add(user)
    await session.commit()
    return user


@pytest.mark.asyncio
async def test_login_access_token(client: AsyncClient, session):
    email = "login_test@example.com"
    password = "password123"
    await create_dummy_user(session, email, password)

    response = await client.post(
        "/token",
        data={"username": email, "password": password}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, session):
    email = "wrong_pass@example.com"
    password = "password123"
    await create_dummy_user(session, email, password)

    response = await client.post(
        "/token",
        data={"username": email, "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"