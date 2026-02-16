from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from app.core.context import Context
from app.utils.extract_fields import extract_fields
from app.utils.extract_fields import extract_fields
from app.graphql.types.chat_room_member_type import ChatRoomMemberType
from sqlalchemy.future import select

from app.utils.get_column import ColumnGetter
from app.utils.validate_fields import validate_fields

@strawberry.type
class ChatRoomMemberQuery:
    @strawberry.field
    async def get_chat_room_members(self, info: strawberry.Info[Context]) -> List[ChatRoomMemberType]:
        try:
            if not validate_fields(info, "chatRoomMember"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in chatRoomMember detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_chat_room_member_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                members = result.mappings().all()  # type: ignore
                return [ChatRoomMemberType(**member) for member in members]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching chat room members: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch chat room members")
