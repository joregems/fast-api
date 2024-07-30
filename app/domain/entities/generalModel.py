from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr, create_model
from pydantic.json_schema import SkipJsonSchema
from typing import List, Optional, Tuple

general_dict = {
  "pk":(SkipJsonSchema[Optional[int]],None),
  "id":(Optional[UUID], None),
  "name":(str, ...),
  "email":(EmailStr, ...),
  "password":(str, ...)
  }

def get_dict_given_dict_and_keys(general_dict:dict, list_of_keys:list)->dict:
  """
  returns the selected keys and values from the given dictionary, and list of keys
  :param general_dict: you give a dict who contains the key and value you need for you new dict
  :param list_of_keys: you pass a list of keys contained in general_dict
  :returns: return a dict with the keys requested
  """
  return dict([(el, general_dict[el]) for el in list_of_keys])
  