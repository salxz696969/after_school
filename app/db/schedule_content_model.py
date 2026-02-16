from typing import TYPE_CHECKING
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .schedule_model import ScheduleModel
    from .media_model import MediaModel


class ScheduleContentModel(Base):
    __tablename__ = "schedule_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=True)
    schedule_id: Mapped[int | None] = mapped_column(
        ForeignKey("schedules.id", ondelete="set null"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    schedule: Mapped["ScheduleModel"] = relationship(
        "ScheduleModel", back_populates="content"
    )
    medias: Mapped[list["MediaModel"]] = relationship(
        "MediaModel", back_populates="schedule_content"
    )
