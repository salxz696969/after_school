from __future__ import annotations
import logging
from fastapi import HTTPException
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.graphql.types.schedule_type import ScheduleType
from app.core.context import Context


@strawberry.type
class ScheduleQuery:
    @strawberry.field
    async def get_schedules(self, info: strawberry.Info[Context]) -> List[ScheduleType]:
        try:
            if not validate_fields(info, "schedule"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in schedule detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_schedule_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                schedules = result.mappings().all()  # type: ignore
                return [ScheduleType(**schedule) for schedule in schedules]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching schedules: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch schedules")
