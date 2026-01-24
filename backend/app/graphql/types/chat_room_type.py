from __future__ import annotations
import enum
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, List
from app.core.context import Context
from sqlalchemy import select
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel

if TYPE_CHECKING:
    from .chat_type import ChatType
    from .chat_room_member_type import ChatRoomMemberType


@strawberry.enum
class ChatRoomTypeEnum(enum.Enum):
    GROUP_CHAT = "group_chat"
    DIRECT_MESSAGE = "direct_message"


@strawberry.type
class ChatRoomType:
    id: int
    chat_room_type: ChatRoomTypeEnum | None = None
    chat_room_name: str | None = None
    avatar_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def chats(self, info: strawberry.Info[Context]) -> List[ChatType]:
        db = info.context.db
        stmt = select(ChatModel).where(ChatModel.chat_room_id == self.id)
        result = await db.execute(stmt)
        chats = result.scalars().all()
        return [
            ChatType(
                id=chat.id,
                chat_room_id=chat.chat_room_id,
                user_id=chat.user_id,
                created_at=chat.created_at,
                updated_at=chat.updated_at,
            )
            for chat in chats
        ]

    @strawberry.field
    async def members(self, info: strawberry.Info[Context]) -> List[ChatRoomMemberType]:
        db = info.context.db
        stmt = select(ChatRoomMemberModel).where(
            ChatRoomMemberModel.chat_room_id == self.id
        )
        result = await db.execute(stmt)
        members = result.scalars().all()
        return [
            ChatRoomMemberType(
                id=member.id,
                chat_room_id=member.chat_room_id,
                user_id=member.user_id,
                created_at=member.created_at,
                updated_at=member.updated_at,
            )
            for member in members
        ]
