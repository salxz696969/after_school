from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .class_model import ClassModel
    from .assignment_model import AssignmentModel
    from .assignment_reply_model import AssignmentReplyModel
    from .announcement_model import AnnouncementModel
    from .chat_model import ChatModel
    from .chat_room_member_model import ChatRoomMemberModel


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
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
        "ClassModel", back_populates="users"
    )
    assignments: Mapped[list["AssignmentModel"]] = relationship(
        "AssignmentModel", back_populates="user"
    )
    assignment_replies: Mapped[list["AssignmentReplyModel"]] = relationship(
        "AssignmentReplyModel", back_populates="user"
    )
    announcements: Mapped[list["AnnouncementModel"]] = relationship(
        "AnnouncementModel", back_populates="user"
    )
    chats: Mapped[list["ChatModel"]] = relationship("ChatModel", back_populates="user")
    chat_room_members: Mapped[list["ChatRoomMemberModel"]] = relationship(
        "ChatRoomMemberModel", back_populates="user"
    )
