from __future__ import annotations
from typing import List
import strawberry

from app.core.context import Context
from app.graphql.types.assignment_type import AssignmentType
from app.utils.extract_fields import extract_fields
from app.utils.get_column import get_assignment_columns


@strawberry.type
class AssignmentQuery:
    @strawberry.field
    async def get_assignments(self, info: strawberry.Info[Context]) -> List[AssignmentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_assignment_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            assignments = result.mappings().all()
            return [AssignmentType(**assignment) for assignment in assignments]  # type: ignore
        except Exception as e:
            raise e