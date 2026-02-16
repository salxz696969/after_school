from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chat_room_model import ChatRoomModel
    from .user_model import UserModel


class ChatRoomMemberModel(Base):
    __tablename__ = "chat_room_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_room_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="set null"), nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="set null"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    chat_room: Mapped["ChatRoomModel"] = relationship(
        "ChatRoomModel", back_populates="members"
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="chat_room_members"
    )
