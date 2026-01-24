from __future__ import annotations
import strawberry
from datetime import datetime
from typing import Annotated, Optional
from typing import TYPE_CHECKING
from app.core.context import Context
from app.graphql.types.chat_room_type import ChatRoomTypeEnum
from app.models.chat_content_model import ChatContentModel
from app.models.chat_room_model import ChatRoomModel
from app.models.user_model import UserModel
from sqlalchemy import select

if TYPE_CHECKING:
    from .chat_room_type import ChatRoomType
    from .user_type import UserType
    from .chat_content_type import ChatContentType


@strawberry.type
class ChatType:
    id: int
    chat_room_id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def chat_room(self, info: strawberry.Info[Context]) -> ChatRoomType:
        db = info.context.db
        stmt = select(ChatRoomModel).where(ChatRoomModel.id == self.chat_room_id)
        result = await db.execute(stmt)
        chat_room = result.scalars().first()
        if chat_room is None:
            raise Exception("Chat room not found")
        return ChatRoomType(
            id=chat_room.id,
            avatar_url=chat_room.avatar_url,
            chat_room_name=chat_room.chat_room_name,
            chat_room_type=ChatRoomTypeEnum[chat_room.chat_room_type],
            created_at=chat_room.created_at,
            updated_at=chat_room.updated_at,
        )

    @strawberry.field
    async def user(self, info: strawberry.Info[Context]) -> UserType:
        db = info.context.db
        stmt = select(UserModel).where(UserModel.id == self.user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user is None:
            raise Exception("User not found")
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url,
            class_id=user.class_id,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @strawberry.field
    async def contents(self, info: strawberry.Info[Context]) -> list[ChatContentType]:
        db = info.context.db
        stmt = select(ChatContentModel).where(ChatContentModel.chat_id == self.id)
        result = await db.execute(stmt)
        contents = result.scalars().all()
        return [
            ChatContentType(
                id=content.id,
                chat_id=content.chat_id,
                created_at=content.created_at,
                updated_at=content.updated_at,
            )
            for content in contents
        ]
