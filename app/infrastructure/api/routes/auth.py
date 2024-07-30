from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from typing import Annotated
from domain.entities import UserPayload

from infrastructure.api.utils.auth import AuthControllerDependency
from infrastructure.api.utils.auth import UserRepository
from infrastructure.api.utils.auth import login_for_access_token

UserControllerDependency = AuthControllerDependency

auth_route = APIRouter(
    tags=["users"]
    )


from fastapi.security import OAuth2PasswordRequestForm


@auth_route.post(f"/login",
        tags=["users"],
        status_code=status.HTTP_200_OK)
async def login_for_access_token_(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        controller: UserControllerDependency,
        repository: UserRepository):
    token =  await login_for_access_token(
        form_data=form_data,
        repository=repository,
        controller=controller
    )
    return token


@auth_route.post(f"/register",
        tags=["users"],
        status_code=status.HTTP_200_OK)
async def register_user(
        user_:UserPayload,
        repository:UserRepository,
        controller:UserControllerDependency):
    user_.role="user"
    return await controller.create(user_, repository)
