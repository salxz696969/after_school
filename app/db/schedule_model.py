from __future__ import annotations
from app.core.database import Base
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .class_model import ClassModel
    from .schedule_content_model import ScheduleContentModel


class ScheduleModel(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    class_id: Mapped[int | None] = mapped_column(
        ForeignKey("classes.id", ondelete="set null"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    class_: Mapped["ClassModel"] = relationship(
        "ClassModel", back_populates="schedules"
    )
    content: Mapped["ScheduleContentModel"] = relationship(
        "ScheduleContentModel",
        back_populates="schedule",
    )
