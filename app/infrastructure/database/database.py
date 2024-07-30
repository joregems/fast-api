from collections.abc import AsyncGenerator
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from settings import DATABASE_URL
from infrastructure.database.model.base import Base

async def get_db_session_general() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(DATABASE_URL)
    factory = async_sessionmaker(async_engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise

async def create_tables_if_not_exists() -> None:
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
