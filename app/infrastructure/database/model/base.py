from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Column
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
import datetime
class Base(DeclarativeBase):
    """Base database model."""
    pk: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
        )

    id: Mapped[UUID] = mapped_column(
        default=uuid4,
        unique=True
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    time_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now())

    # updated_at: Mapped[datetime.datetime] = mapped_column(
    #     DateTime(timezone=True),
    #     onupdate=func.now
    # )


