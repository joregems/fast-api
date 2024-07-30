from ..generic_interactors import CreateEntityUseCase
from ..generic_interactors import UpdateEntityUseCase
from ...interfaces.useCases import EntityUseCasesInterface
from ..generic_interactors import GetEntityUseCase
from ..generic_interactors import GetAllEntitiesUseCase
from ..generic_interactors import DeleteEntityUseCase
from typing import Callable, TypeVar, Generic
from domain.entities.user import UserPayload

PasswordHasher=Callable[[str], str]
ModelDB = TypeVar('ModelDB')

class CreateUserUseCase(CreateEntityUseCase):
  def __init__(self, repository: EntityUseCasesInterface, passwordHasher:PasswordHasher):
    super().__init__(repository)
    self.passwordHasher=passwordHasher
  async def execute(self, user_payload: UserPayload) -> ModelDB:
    user_payload.password = self.passwordHasher(user_payload.password)
    return await self.repository.create(user_payload)


class UpdateUserUseCase(UpdateEntityUseCase):
  def __init__(self, repository: EntityUseCasesInterface, passwordHasher:PasswordHasher):
    super().__init__(repository)
    self.passwordHasher=passwordHasher
  async def execute(self, id, user_payload: UserPayload) -> ModelDB:
    user_payload.password = self.passwordHasher(user_payload.password)
    return await self.repository.update(id,user_payload)
