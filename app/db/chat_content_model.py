from typing import TYPE_CHECKING
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .chat_model import ChatModel
    from .media_model import MediaModel


class ChatContentModel(Base):
    __tablename__ = "chat_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(nullable=True)
    chat_id: Mapped[int | None] = mapped_column(
        ForeignKey("chats.id", ondelete="set null"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    chat: Mapped["ChatModel"] = relationship("ChatModel", back_populates="content")
    medias: Mapped[list["MediaModel"]] = relationship(
        "MediaModel", back_populates="chat_content"
    )
