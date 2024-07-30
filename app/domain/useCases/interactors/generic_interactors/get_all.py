
from typing import Generic, TypeVar, List
from domain.entities.user import User
from ...interfaces.useCases import EntityUseCasesInterface

ModelDB = TypeVar('ModelDB')

class GetAllEntitiesUseCase(Generic[ModelDB]):
    def __init__(self, repository: EntityUseCasesInterface):
        self.repository = repository

    async def execute(self) -> List[ModelDB]:
        return await self.repository.get_all()
