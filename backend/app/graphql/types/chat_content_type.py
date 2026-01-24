from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from sqlalchemy import select
from app.models.chat_model import ChatModel
from app.models.media_model import MediaModel
from typing import TYPE_CHECKING, Annotated, List

if TYPE_CHECKING:
    from .chat_type import ChatType
    from .media_type import MediaType


@strawberry.type
class ChatContentType:
    id: int
    chat_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def chat(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatType",
        strawberry.lazy("app.graphql.types.chat_type"),
    ]:
        from app.graphql.types.chat_type import ChatType
        db = info.context.db
        stmt = select(ChatModel).where(ChatModel.id == self.chat_id)
        result = await db.execute(stmt)
        chat = result.scalars().first()
        if chat is None:
            raise Exception("Chat not found")
        return ChatType(
            id=chat.id,
            user_id=chat.user_id,
            chat_room_id=chat.chat_room_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

    @strawberry.field
    async def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        from app.graphql.types.media_type import MediaType
        db = info.context.db
        stmt = select(MediaModel).where(MediaModel.chat_content_id == self.id)
        result = await db.execute(stmt)
        medias = result.scalars().all()
        return [
            MediaType(
                id=media.id,
                chat_content_id=media.chat_content_id,
                url=media.url,
                created_at=media.created_at,
                updated_at=media.updated_at,
            )
            for media in medias
        ]
