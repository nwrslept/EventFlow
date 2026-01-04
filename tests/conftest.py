import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.config import settings
from app.core.database import get_db
from app.models.base import Base
from app.core.security import create_access_token


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(settings.DATABASE_URL, connect_args={"ssl": False})

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def authorized_client(client: AsyncClient, session: AsyncSession):
    from app.models.user import User
    from app.core.security import get_password_hash

    user_email = "auth_user@example.com"
    user_password = "password123"
    hashed_password = get_password_hash(user_password)

    user = User(email=user_email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    access_token = create_access_token(data={"sub": user.email})

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }

    return client