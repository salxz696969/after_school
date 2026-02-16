from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .class_model import ClassModel
    from .assignment_model import AssignmentModel


class SubjectModel(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    class_id: Mapped[int | None] = mapped_column(
        ForeignKey("classes.id", ondelete="set null"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    class_: Mapped["ClassModel"] = relationship(
        "ClassModel", back_populates="subjects"
    )
    assignments: Mapped[list["AssignmentModel"]] = relationship(
        "AssignmentModel", back_populates="subject"
    )
