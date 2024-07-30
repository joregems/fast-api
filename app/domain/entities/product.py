from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema
from enum import Enum
from typing import List, Optional, Tuple

class Config:
  # orm_mode = True
  from_attributes=True

class Product(BaseModel):
  name: str
  description: str
  sku: str
  coverImage : str
  price: float
  __config__=Config
