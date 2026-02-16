from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.assignment_reply_type import AssignmentReplyType


@strawberry.type
class AssignmentReplyQuery:
    @strawberry.field
    async def get_assignment_replies(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentReplyType]:
        try:
            if not validate_fields(info, "assignmentReply"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in assignmentReply detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_assignment_reply_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                replies = result.mappings().all()  # type: ignore
                return [AssignmentReplyType(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching assignment replies: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch assignment replies"
            )
