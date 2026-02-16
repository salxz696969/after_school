from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.assignment_reply_content_type import AssignmentReplyContentType
from fastapi import HTTPException
import logging


@strawberry.type
class AssignmentReplyContentQuery:
    @strawberry.field
    async def get_reply_contents(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentReplyContentType]:
        try:
            if not validate_fields(info, "assignmentReplyContent"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in assignmentReplyContent detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_assignment_reply_content_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AssignmentReplyContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching assignment reply contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch assignment reply contents"
            )
