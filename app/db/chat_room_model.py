from __future__ import annotations
import enum
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Integer, String
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .chat_model import ChatModel
    from .chat_room_member_model import ChatRoomMemberModel


class ChatRoomType(str, enum.Enum):
    GROUP_CHAT = "group_chat"
    DIRECT_MESSAGE = "direct_message"


class ChatRoomModel(Base):
    __tablename__ = "chat_rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_room_type: Mapped[ChatRoomType] = mapped_column(
        String, nullable=False
    )
    chat_room_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    chats: Mapped[list["ChatModel"]] = relationship(
        "ChatModel", back_populates="chat_room"
    )
    members: Mapped[list["ChatRoomMemberModel"]] = relationship(
        "ChatRoomMemberModel", back_populates="chat_room"
    )
