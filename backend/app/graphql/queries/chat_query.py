from __future__ import annotations
import strawberry
from typing import List
from sqlalchemy import select
from app.utils import extract_fields
from app.utils.get_column import get_chat_columns
from app.core.context import Context
from app.graphql.types.chat_type import ChatType


@strawberry.type
class ChatQuery:
    @strawberry.field
    async def get_chats(self, info: strawberry.Info[Context]) -> List[ChatType]:
        try:
            fields = extract_fields(info)
            column_dict = get_chat_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            chats = result.mappings().all()
            return [ChatType(**chat) for chat in chats]  # type: ignore
        except Exception as e:
            raise e
