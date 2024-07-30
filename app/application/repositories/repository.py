import uuid
from typing import Generic, TypeVar
from domain.useCases.interfaces.useCases import EntityUseCasesInterface
from sqlalchemy import BinaryExpression, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


ModelDB = TypeVar("ModelDB")
PayloadModel = TypeVar("PayloadModel", bound=BaseModel)


class DatabaseRepository(Generic[ModelDB], EntityUseCasesInterface):
    """Repository for performing database queries."""

    def __init__(self, model: type[ModelDB], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: PayloadModel) -> ModelDB:
        instance = self.model(**jsonable_encoder(data))
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, id: uuid.UUID) -> ModelDB | None:
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.one_or_none()[0]

    async def get_all(self) -> list[ModelDB] | None:
        result = await self.session.execute(select(self.model))
        rows = result.scalars().all()
        return rows

    async def update(self, id: uuid.UUID, data: PayloadModel) -> ModelDB | None:
        stmt= (select(self.model)
            .where(self.model.id == id))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        for key, value in jsonable_encoder(data).items():
            if value:
                setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: uuid.UUID) -> ModelDB | None:
        delete_stmt = (
        delete(self.model)
        .where(getattr(self.model, 'id') == id)
        .returning(self.model))
        result = await self.session.execute(delete_stmt)
        item_for_deletion = result.one_or_none()[0]
        self.session.expunge(item_for_deletion)
        await self.session.commit()
        return item_for_deletion

    async def filter(
        self,
        query_dict: dict,
    ) -> list[ModelDB]:
        query = select(self.model)
        expressions = []
        for key in query_dict.keys():
            attribute_db = getattr(self.model, key)
            operation = getattr(attribute_db, query_dict[key]["operation"])
            expressions.append(operation(query_dict[key]["value"]))

        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))
