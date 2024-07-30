from collections.abc import Callable
from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import DatabaseRepository
from typing import TypeVar
ModelDB = TypeVar('ModelDB')
def get_repository(
    model: ModelDB,
    get_session:AsyncGenerator[AsyncSession, None]
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_session)):
        return DatabaseRepository(model, session)

    return func
