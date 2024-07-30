from typing import Generic, TypeVar
from domain.entities.user import User
from ...interfaces.useCases import EntityUseCasesInterface
from uuid import UUID
ModelDB = TypeVar('ModelDB')

class DeleteEntityUseCase(Generic[ModelDB]):
    def __init__(self, repository: EntityUseCasesInterface):
        self.repository = repository

    async def execute(self, id: UUID) -> ModelDB:
        return await self.repository.delete(id=id)
