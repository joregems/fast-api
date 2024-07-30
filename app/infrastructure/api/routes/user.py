from fastapi import APIRouter
from typing import Annotated
from fastapi import HTTPException, Depends, status
from infrastructure.database.model.user import UserDB
from infrastructure.database.database import get_db_session_general
# from domain.entities import UserPayload
# from domain.entities import UserPresent
from application.repositories.dependencies import get_repository
from application.repositories.repository import DatabaseRepository
from application.controllers.user import UserController
from domain.entities.user import UserPresent
from domain.entities.user import UserPayload
from domain.entities.user import User
from uuid import UUID
from infrastructure.utils.optional_models import partial_model
from infrastructure.api.utils.auth import authorize
from infrastructure.api.utils.auth import get_current_active_user
from infrastructure.api.utils.auth import AuthControllerDependency
from infrastructure.api.utils.auth import UserRepository
from infrastructure.api.utils.auth import login_for_access_token

user_route = APIRouter(
    tags=["users"]
    )

UserControllerDependency = AuthControllerDependency
end_route =""


@user_route.post(f"/{end_route}",
        tags=["users"],
        status_code=status.HTTP_201_CREATED, response_model=UserPresent)
@authorize(role=["admin"])
async def create_user(
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        user_:UserPayload,
        repository:UserRepository,
        controller:UserControllerDependency):
    return await controller.create(user_, repository)


@user_route.get(f"/{end_route}",
    tags=["users"],
    response_model=list[UserPresent],
    status_code=status.HTTP_200_OK)
@authorize(role=["admin"])
async def list_users(
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        repository: UserRepository,
        controller:UserControllerDependency
        )->list[UserPresent]:
    return await controller.get_all(response_model=UserPresent, repository=repository)


@user_route.get(f"/me",
                tags=["users"],
                response_model=UserPresent)
@authorize(role=["admin"])
async def read_users_me(
        current_user: Annotated[UserPresent, Depends(get_current_active_user)]
        )->UserPresent:
    return current_user


@user_route.get(f"/"+"{id}",
        tags=["users"],
        status_code=status.HTTP_200_OK)
@authorize(role=["admin"])
async def get_user(
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        id:UUID,
        repository: UserRepository,
        controller:UserControllerDependency
        )->UserPresent:
    return await controller.get(id=id, response_model=UserPresent, repository=repository)


@user_route.get(f"/email/"+"{email}",
        tags=["users"],
        status_code=status.HTTP_200_OK)
@authorize(role=["admin"])
async def get_email(
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        email:str,
        repository: UserRepository,
        controller:UserControllerDependency
        )->UserPresent:
    # query_dict = {"id":{"operation":"__eq__", "value":id}}
    result = await controller.filter(query={"email":{"operation":"__eq__", "value":email}},
        response_model=UserPresent,repository=repository)
    return result[0]


@partial_model
class NewUserPayload(UserPayload):
    pass

@authorize(role=["admin"])
@user_route.put(f"/"+"{id}",

        tags=["users"],
        response_model=UserPresent,
        status_code=status.HTTP_200_OK)
async def update_user(
        id:UUID,
        user_:NewUserPayload,
        repository: UserRepository,
        controller:UserControllerDependency,
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        )->UserPresent:
    return await controller.update(id=id,user_=user_,repository=repository)

@authorize(role=["admin"])
@user_route.delete(f"/"+"{id}",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserPresent)
async def delete_user(
        id:UUID,
        repository: UserRepository,
        controller:UserControllerDependency,
        current_user: Annotated[UserPresent, Depends(get_current_active_user)],
        )->UserPresent:
    return await controller.delete(id=id,response_model=UserPresent, repository=repository)
