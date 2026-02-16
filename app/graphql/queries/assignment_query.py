from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy import select
from app.core.context import Context
from app.graphql.types.assignment_type import AssignmentType
from app.utils import validate_fields
from app.utils.extract_fields import extract_fields
from app.utils.get_column import ColumnGetter


@strawberry.type
class AssignmentQuery:
    @strawberry.field
    async def get_assignments(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentType]:
        try:
            if not validate_fields(info, "assignment"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in assignment detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_assignment_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignments = result.mappings().all()  # type: ignore
                return [AssignmentType(**assignment) for assignment in assignments]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch assignments")
