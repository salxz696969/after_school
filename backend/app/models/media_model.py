from sqlalchemy import ForeignKey
from app.core.database import Base
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .assignment_reply_content_model import AssignmentReplyContentModel
    from .announcement_content_model import AnnouncementContentModel
    from .schedule_content_model import ScheduleContentModel
    from .chat_content_model import ChatContentModel
    from .assignment_content_model import AssignmentContentModel


class MediaModel(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    chat_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_contents.id", ondelete="set null"), nullable=True
    )
    schedule_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("schedule_contents.id", ondelete="set null"), nullable=True
    )
    announcement_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("announcement_contents.id", ondelete="set null"), nullable=True
    )
    assignment_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignment_contents.id", ondelete="set null"), nullable=True
    )
    assignment_reply_content_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignment_reply_contents.id", ondelete="set null"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    schedule_content: Mapped["ScheduleContentModel"] = relationship(
        "ScheduleContentModel", back_populates="medias"
    )
    announcement_content: Mapped["AnnouncementContentModel"] = relationship(
        "AnnouncementContentModel", back_populates="medias"
    )
    assignment_content: Mapped["AssignmentContentModel"] = relationship(
        "AssignmentContentModel", back_populates="medias"
    )
    assignment_reply_content: Mapped["AssignmentReplyContentModel"] = relationship(
        "AssignmentReplyContentModel", back_populates="medias"
    )
    chat_content: Mapped["ChatContentModel"] = relationship(
        "ChatContentModel", back_populates="medias"
    )
