from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.assignment_content_type import AssignmentContentType


@strawberry.type
class AssignmentContentQuery:
    @strawberry.field
    async def get_assignment_contents(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentContentType]:
        try:
            if not validate_fields(info, "assignmentContent"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in assignmentContent detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_assignment_content_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AssignmentContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching assignment contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch assignment contents"
            )
