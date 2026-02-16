from typing import TYPE_CHECKING
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .announcement_model import AnnouncementModel
    from .media_model import MediaModel


class AnnouncementContentModel(Base):
    __tablename__ = "announcement_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=True)
    announcement_id: Mapped[int | None] = mapped_column(
        ForeignKey("announcements.id", ondelete="set null"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    announcement: Mapped["AnnouncementModel"] = relationship(
        "AnnouncementModel", back_populates="content"
    )
    medias: Mapped[list["MediaModel"]] = relationship(
        "MediaModel", back_populates="announcement_content"
    )
