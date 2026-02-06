from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy import select
from app.utils import extract_fields
from app.utils.get_column import get_assignment_content_columns
from app.core.context import Context
from app.graphql.types.assignment_content_type import AssignmentContentType


@strawberry.type
class AssignmentContentQuery:
    @strawberry.field
    async def get_assignment_contents(self, info : strawberry.Info[Context]) -> List[AssignmentContentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_assignment_content_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AssignmentContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
