from __future__ import annotations
import logging
from fastapi import HTTPException
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.schedule_content_type import ScheduleContentType


@strawberry.type
class ScheduleContentQuery:
    @strawberry.field
    async def get_schedule_contents(
        self, info: strawberry.Info[Context]
    ) -> List[ScheduleContentType]:
        try:
            if not validate_fields(info, "scheduleContent"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in schedule_content detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_schedule_content_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                schedule_contents = result.mappings().all()  # type: ignore
                return [ScheduleContentType(**schedule_content) for schedule_content in schedule_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching schedule contents: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch schedule contents")
