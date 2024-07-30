from sqlalchemy import String
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
# from orm.orm_utils import GUID

class UserDB(Base):
  __tablename__ = 'users'
  # id = Column(Integer, primary_key=True, index=True)
  # uuid = Column(GUID(), unique=True, default=lambda: str(uuid.uuid4()), index=True)
  name: Mapped[str]
  password: Mapped[str]
  email: Mapped[str]=mapped_column(String, unique=True, index=False)
  role:Mapped[str]=mapped_column(String, index=True)