from domain.useCases.interactors.user import CreateUserUseCase
from domain.useCases.interactors.user import UpdateUserUseCase
from infrastructure.utils.cryptography import password_hasher
from domain.entities import UserPayload
from domain.entities import UserPresent
from typing import TypeVar
from .general_controller import GeneralController
from uuid import UUID

UserRepository = TypeVar('UserRepository')

class UserController(GeneralController):


    async def create(
            self,
            user_:UserPayload,
            repository: UserRepository
            )->UserPresent:
        create_user_use_case = CreateUserUseCase(repository, password_hasher)
        db_user = await create_user_use_case.execute(user_)
        return UserPresent.model_validate(db_user)


    async def update(
            self,
            id:UUID,
            user_:UserPayload,
            repository: UserRepository
            )->UserPresent:
        update_user_use_case = UpdateUserUseCase(repository, password_hasher)
        db_user = await update_user_use_case.execute(id, user_)
        return UserPresent.model_validate(db_user)
