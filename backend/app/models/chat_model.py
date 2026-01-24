from __future__ import annotations
from sqlalchemy import Integer
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_model import UserModel
    from .chat_room_model import ChatRoomModel
    from .chat_content_model import ChatContentModel


class ChatModel(Base):
    __tablename__ = "chats"

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
        "ChatRoomModel", back_populates="chats"
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="chats")
    content: Mapped["ChatContentModel"] = relationship(
        "ChatContentModel", back_populates="chat"
    )
