from __future__ import annotations
import logging
from fastapi import HTTPException
import strawberry
from typing import List
from sqlalchemy import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.chat_type import ChatType


@strawberry.type
class ChatQuery:
    @strawberry.field
    async def get_chats(self, info: strawberry.Info[Context]) -> List[ChatType]:
        try:
            if not validate_fields(info, "chat"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in chat detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_chat_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chats = result.mappings().all()  # type: ignore
                return [ChatType(**chat) for chat in chats]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching chats: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch chats")
