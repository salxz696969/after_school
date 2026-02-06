from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy import select
from app.utils import extract_fields
from app.utils.get_column import get_assignment_reply_columns
from app.core.context import Context
from app.graphql.types.assignment_reply_type import AssignmentReplyType

@strawberry.type
class AssignmentReplyQuery:
    @strawberry.field
    async def get_assignment_replies(self, info: strawberry.Info[Context]) -> List[AssignmentReplyType]:
        try:
            fields = extract_fields(info)
            column_dict = get_assignment_reply_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            replies = result.mappings().all()
            return [AssignmentReplyType(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            raise e
