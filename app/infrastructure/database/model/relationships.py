import uuid
from .base import Base

from sqlalchemy import Column, ForeignKey, Table, orm
# from sqlalchemy.dialects.postgresql import UUID
# from uuid import UUID, uuid4

# potion_ingredient_association = Table(
#     "potion_ingredient",
#     Base.metadata,
#     # Column("potion_id", UUID(as_uuid=True), ForeignKey("potion.pk")),
#     # Column("ingredient_id", UUID(as_uuid=True), ForeignKey("ingredient.pk")),
# )