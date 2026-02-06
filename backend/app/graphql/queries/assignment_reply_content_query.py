from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy import select
from app.utils import extract_fields
from app.utils.get_column import get_assignment_reply_content_columns
from app.core.context import Context
from app.graphql.types.assignment_reply_content_type import AssignmentReplyContentType


@strawberry.type
class AssignmentReplyContentQuery:
    @strawberry.field
    async def get_reply_contents(self, info: strawberry.Info[Context]) -> List[AssignmentReplyContentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_assignment_reply_content_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AssignmentReplyContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
