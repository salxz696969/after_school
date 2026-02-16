from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .assignment_model import AssignmentModel
    from .user_model import UserModel
    from .assignment_reply_content_model import AssignmentReplyContentModel


class AssignmentReplyModel(Base):
    __tablename__ = "assignment_replies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assignment_id: Mapped[int | None] = mapped_column(
        ForeignKey("assignments.id", ondelete="set null"), nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="set null"), nullable=True
    )
    up_vote: Mapped[int] = mapped_column(Integer, default=0)
    down_vote: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    assignment: Mapped["AssignmentModel"] = relationship(
        "AssignmentModel", back_populates="replies"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="assignment_replies"
    )
    content: Mapped["AssignmentReplyContentModel"] = relationship(
        "AssignmentReplyContentModel",
        back_populates="assignment_reply",
    )
