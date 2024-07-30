from typing import Generic, TypeVar
from domain.entities.user import User
from ...interfaces.useCases import EntityUseCasesInterface
from uuid import UUID
from pydantic import BaseModel

ModelDB = TypeVar('ModelDB')
PayloadModel = TypeVar('PayloadModel', bound= BaseModel)
class UpdateEntityUseCase(Generic[ModelDB]):
    def __init__(self, repository: EntityUseCasesInterface):
        self.repository = repository

    async def execute(self, id:UUID, entity: PayloadModel) -> ModelDB:
        return await self.repository.update(id, entity)

