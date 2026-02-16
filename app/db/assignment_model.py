from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .user_model import UserModel
    from .subject_model import SubjectModel
    from .class_model import ClassModel
    from .assignment_reply_model import AssignmentReplyModel
    from .assignment_content_model import AssignmentContentModel


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="set null"), nullable=True
    )
    subject_id: Mapped[int | None] = mapped_column(
        ForeignKey("subjects.id", ondelete="set null"), nullable=True
    )
    class_id: Mapped[int | None] = mapped_column(
        ForeignKey("classes.id", ondelete="set null"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped[UserModel] = relationship("UserModel", back_populates="assignments")
    subject: Mapped["SubjectModel"] = relationship(
        "SubjectModel", back_populates="assignments"
    )
    class_: Mapped["ClassModel"] = relationship(
        "ClassModel", back_populates="assignments"
    )
    replies: Mapped[list["AssignmentReplyModel"]] = relationship(
        "AssignmentReplyModel", back_populates="assignment"
    )
    content: Mapped["AssignmentContentModel"] = relationship(
        "AssignmentContentModel",
        back_populates="assignment",
    )
