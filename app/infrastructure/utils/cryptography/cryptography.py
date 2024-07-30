from passlib.context import CryptContext
from typing import TypeVar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HashedPassword = TypeVar('HashedPassword', bound=str)
Password = TypeVar('Password', str, None)

def verify_password(plain_password:Password, hashed_password:HashedPassword)->bool:
    """
    compare a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def password_hasher(password:Password)->HashedPassword:
    """
    hash a plain password
    """
    # hashed_pass = None
    # try:
    #     hashed_pass = pwd_context.hash(password)
    # except:
    #     pass
    

    hashed_pass = None
    if password:
        hashed_pass = pwd_context.hash(password)
    return hashed_pass