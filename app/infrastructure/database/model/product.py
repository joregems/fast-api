from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
# from orm.orm_utils import GUID

class Product(Base):
  __tablename__ = 'products'
  name: Mapped[str]= mapped_column(String, nullable=False, index=True)
  description: Mapped[str]= mapped_column(String, nullable=False, index=False)
  sku: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=False)
  coverImage : Mapped[str]
  price: Mapped[float]= mapped_column(String, nullable=False, index=False)
