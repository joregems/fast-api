from typing import Generic, TypeVar
from ...interfaces.useCases import EntityUseCasesInterface
from uuid import UUID

ModelDB = TypeVar('ModelDB')

class GetEntityUseCase(Generic[ModelDB]):
    def __init__(self, repository: EntityUseCasesInterface):
        self.repository = repository

    async def execute(self, id: UUID) -> ModelDB:
        result = await self.repository.filter({"id":{"operation":"__eq__", "value":id}})
        return result[0]
