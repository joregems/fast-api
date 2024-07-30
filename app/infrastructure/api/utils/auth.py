from datetime import timedelta
from fastapi import APIRouter
from typing import Annotated
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from fastapi import Header
from infrastructure.database.model.user import UserDB
from infrastructure.utils.jwtokens import ConfigToken
from infrastructure.utils.jwtokens import decode_token
from application.repositories.dependencies import get_repository
from application.repositories.repository import DatabaseRepository
from infrastructure.database.database import get_db_session_general
from infrastructure.utils.jwtokens import create_token as create_tokenCustom

from domain.entities.user import UserPresent
from domain.entities.user import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from infrastructure.utils.cryptography import verify_password
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from dataclasses import dataclass
from typing import TypeVar
from application.controllers.user import UserController

UserRepository = Annotated[
    DatabaseRepository[UserDB],
    Depends(get_repository(UserDB, get_db_session_general))]

AuthControllerDependency = Annotated[UserController, Depends(UserController)]

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 200
REFRESH_TOKEN_EXPIRE_MINUTES = 1440
DEFAULT_TOKEN_EXPIRE_MINUTES = 200

class Credentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

from functools import wraps
from fastapi import HTTPException

def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get("current_user").role
            if user_role not in role:
                raise HTTPException(status_code=403, detail="User is not authorized to access")
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_config(expires_delta=None):
    return ConfigToken(
        expires_delta=expires_delta,
        DEFAULT_TOKEN_EXPIRE_MINUTES=DEFAULT_TOKEN_EXPIRE_MINUTES,
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM)


auth_route = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

Controller = TypeVar("Controller")
Repository = TypeVar("Repository")
ResponseModel=TypeVar("ResponseModel")

end_route ="token"

@dataclass
class CustomQuery:
    T = TypeVar("T")
    key:str
    operation:str
    value:T


#should this be a function in a more general library?
async def get_user_with_custom_query(
            controller:Controller,
            repository: Repository,
            query:CustomQuery,
            response_model:ResponseModel
        )->ResponseModel|None:
        user_db = await controller.filter(
            query={query.key:{"operation":query.operation, "value":query.value}},
            response_model=response_model,
            repository=repository)
        if not user_db:
            return None
        return user_db[0]


def get_bearer_token(token: Annotated[str | None, Header(alias='Authorization')] = None):
    print(token, "token")
    try:
        token = token.replace("Bearer ", "")
    except:
        pass
    return token


async def get_current_user_from_authorization_token(
        repository: UserRepository,
        controller: AuthControllerDependency,
        token: Annotated[str, Depends(oauth2_scheme)]
        # token: Annotated[str | None, Depends(get_bearer_token)] = None,
        # token: Annotated[str | None, Cookie(alias='access_token')] = None
        )->User|None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = decode_token(token, config=get_config())
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_with_custom_query(
        repository= repository,
        controller=controller,
        response_model=UserPresent,
        query= CustomQuery("email","__eq__", token_data.username))
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user_from_authorization_token)]):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_token(data: dict, expires_delta: timedelta | None = None):
    return create_tokenCustom(data,config=get_config(expires_delta=expires_delta))


async def verify_credentials(
        credentials:Credentials,
        repository: Repository,
        controller: Controller
        ):
    creds_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    user = await get_user_with_custom_query(
        controller=controller,
        repository=repository,
        response_model=User,
        query=CustomQuery("email","__eq__",credentials.username)
    )
    if not user:
        raise creds_error

    if not verify_password(credentials.password, user.password):
        raise creds_error
    return user


async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        repository: Repository,
        controller: Controller,
        )->Token:
    user = await verify_credentials(
        credentials=Credentials(username=form_data.username,password=form_data.password),
        repository=repository,
        controller=controller
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=250)
    )

    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer")
    return token


from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


async def basic_http_log_in(
        controller: AuthControllerDependency,
        repository: UserRepository,
        credentials: HTTPBasicCredentials = Depends(security),
        ) -> str:
    user = await verify_credentials(
        controller= controller,
        repository= repository,
        credentials= Credentials(
            username=credentials.username,
            password=credentials.password)
    )
    return user.email
