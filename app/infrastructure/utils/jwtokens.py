import jwt
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

@dataclass
class ConfigToken:
  expires_delta: timedelta | None = None
  DEFAULT_TOKEN_EXPIRE_MINUTES:int=15
  SECRET_KEY:str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM:str = "HS256"

def create_token(data: dict, config: ConfigToken):
    to_encode = data.copy()
    if config.expires_delta:
        expire = datetime.now(timezone.utc) + config.expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.DEFAULT_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

# async def decode_token(token, config: ConfigToken):
#     print(token, config,"decode", config.ALGORITHM, config.SECRET_KEY)
def decode_token(token, config: ConfigToken):
    # print(token, config,"decode", config.ALGORITHM, config.SECRET_KEY)
    result = None
    try:
        result=jwt.decode(jwt=token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except Exception as e:
        raise e
    return result