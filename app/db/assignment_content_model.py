from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .assignment_model import AssignmentModel
    from .media_model import MediaModel


class AssignmentContentModel(Base):
    __tablename__ = "assignment_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=True)
    assignment_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignments.id", ondelete="set null"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    assignment: Mapped["AssignmentModel"] = relationship(
        "AssignmentModel", back_populates="content"
    )
    medias: Mapped[list["MediaModel"]] = relationship(
        "MediaModel", back_populates="assignment_content"
    )
