import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.core.config import settings
from app.core.database import get_db
from app.models.base import Base


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