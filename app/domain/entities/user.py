from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr, create_model
from pydantic.json_schema import SkipJsonSchema
from enum import Enum
from typing import List, Optional, Tuple
from .generalModel import get_dict_given_dict_and_keys
from .generalModel import general_dict

class role_typeEnum(str, Enum):
  user = 'user'
  admin = 'admin'

specific_dict = {"role":(role_typeEnum, role_typeEnum.user)}
general_user_dict = {}
general_user_dict.update(general_dict)
general_user_dict.update(specific_dict)

class Config:
  # orm_mode = True
  from_attributes=True

# class User(BaseModel):
#   id: SkipJsonSchema[Optional[int]] = None
#   uuid: Optional[UUID] = None
#   name: str
#   password: str
#   email: EmailStr
#   role: role_typeEnum = role_typeEnum.user
#   class Config:
#     # orm_mode = True
#     from_attributes=True

core_attributes=["name","email","role"]
technical_attributes=["pk"]
present_attributes = ["id"]
payload_Attributes = ["password"]
user_model = create_model(
    'User',
    **get_dict_given_dict_and_keys(general_user_dict, technical_attributes + present_attributes + payload_Attributes + core_attributes),
    __config__=Config)

user_model_payload = create_model(
    'UserPayload',
    **get_dict_given_dict_and_keys(general_user_dict, core_attributes + payload_Attributes),
    __config__=Config)

user_model_present = create_model(
    'UserPresent',
    **get_dict_given_dict_and_keys(general_user_dict, present_attributes + core_attributes),
    __config__=Config)
def create():
  class_model = type('User', (user_model,),{})
  class_model_payload = type('UserPayload', (user_model_payload,),{})
  class_model_present = type('UserPresent', (user_model_present,),{})
  return class_model, class_model_payload, class_model_present

User, UserPayload, UserPresent = create()

class UserList(BaseModel):
  users: List[User]
  # pages: int
  pass
