from __future__ import annotations
from typing import List
import strawberry
from app.core.context import Context
from app.utils.extract_fields import extract_fields
from app.utils.extract_fields import extract_fields
from app.utils.get_column import get_chat_room_member_columns
from app.utils.get_column import get_chat_room_member_columns
from app.graphql.types.chat_room_member_type import ChatRoomMemberType


@strawberry.type
class ChatRoomMemberQuery:
    @strawberry.field
    async def get_chat_room_members(self, info: strawberry.Info[Context]) -> List[ChatRoomMemberType]:
        try:
            fields = extract_fields(info)
            column_dict = get_chat_room_member_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            members = result.mappings().all()
            return [ChatRoomMemberType(**member) for member in members]  # type: ignore
        except Exception as e:
            raise e
