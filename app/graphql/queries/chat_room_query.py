from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy.future import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.chat_room_type import ChatRoomType


@strawberry.type
class ChatRoomQuery:
    @strawberry.field
    async def get_chat_rooms(self, info: strawberry.Info[Context]) -> List[ChatRoomType]:
        try:
            if not validate_fields(info, "chatRoom"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in chatRoom detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_chat_room_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chat_rooms = result.mappings().all()  # type: ignore
                return [ChatRoomType(**chat_room) for chat_room in chat_rooms]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching chat rooms: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch chat rooms")
