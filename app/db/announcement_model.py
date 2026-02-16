from __future__ import annotations
import enum
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, ForeignKey, String
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .user_model import UserModel
    from .class_model import ClassModel
    from .announcement_content_model import AnnouncementContentModel


class AnnouncementTypeStatus(str, enum.Enum):
    GENERAL = "general"
    LEAKS = "leaks"


class AnnouncementModel(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="set null"), nullable=True
    )
    class_id: Mapped[int | None] = mapped_column(
        ForeignKey("classes.id", ondelete="set null"), nullable=True
    )
    type: Mapped[str] = mapped_column(
        String, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="announcements"
    )
    class_: Mapped["ClassModel"] = relationship(
        "ClassModel", back_populates="announcements"
    )

    content: Mapped["AnnouncementContentModel"] = relationship(
        "AnnouncementContentModel",
        back_populates="announcement",
    )
