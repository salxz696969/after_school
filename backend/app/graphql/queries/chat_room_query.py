from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy.future import select
from app.utils import extract_fields
from app.utils.get_column import get_chat_room_columns
from app.core.context import Context
from app.graphql.types.chat_room_type import ChatRoomType


@strawberry.type
class ChatRoomQuery:
    @strawberry.field
    async def get_chat_rooms(self, info: strawberry.Info[Context]) -> List[ChatRoomType]:
        try:
            fields = extract_fields(info)
            column_dict = get_chat_room_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            chat_rooms = result.mappings().all()
            return [ChatRoomType(**chat_room) for chat_room in chat_rooms]  # type: ignore
        except Exception as e:
            raise e
