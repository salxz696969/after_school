from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .assignment_reply_model import AssignmentReplyModel
    from .media_model import MediaModel


class AssignmentReplyContentModel(Base):
    __tablename__ = "assignment_reply_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=True)
    assignment_reply_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignment_replies.id", ondelete="set null"),
        nullable=True,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    assignment_reply: Mapped["AssignmentReplyModel"] = relationship(
        "AssignmentReplyModel", back_populates="content"
    )
    medias: Mapped[list["MediaModel"]] = relationship(
        "MediaModel", back_populates="assignment_reply_content"
    )
