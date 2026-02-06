from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy import select
from app.utils import extract_fields
from app.utils.get_column import get_chat_content_columns
from app.core.context import Context
from app.graphql.types.chat_content_type import ChatContentType


@strawberry.type
class ChatContentQuery:
    @strawberry.field
    async def get_chat_contents(self, info: strawberry.Info[Context]) -> List[ChatContentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_chat_content_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [ChatContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
