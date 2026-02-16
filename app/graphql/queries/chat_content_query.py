from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.chat_content_type import ChatContentType


@strawberry.type
class ChatContentQuery:
    @strawberry.field
    async def get_chat_contents(
        self, info: strawberry.Info[Context]
    ) -> List[ChatContentType]:
        try:
            if not validate_fields(info, "chatContent"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in chatContent detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_chat_content_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [ChatContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching chat contents: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch chat contents")
