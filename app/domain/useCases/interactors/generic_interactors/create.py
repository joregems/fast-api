from typing import Generic, TypeVar
from domain.entities.user import User
# from application.repositories.generic_repository import GenericRepository
from ...interfaces.useCases import EntityUseCasesInterface
from pydantic import BaseModel
ModelDB = TypeVar('ModelDB')
PayloadModel = TypeVar('PayloadModel', bound= BaseModel)

class CreateEntityUseCase(Generic[ModelDB]):
    def __init__(self, repository: EntityUseCasesInterface):
        self.repository = repository

    async def execute(self, entity: PayloadModel) -> ModelDB:
        return await self.repository.create(entity)
