from __future__ import annotations
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields
from app.utils.get_column import get_schedule_columns
from app.graphql.types.schedule_type import ScheduleType
from app.core.context import Context


@strawberry.type
class ScheduleQuery:
    @strawberry.field
    async def get_schedules(self, info: strawberry.Info[Context]) -> List[ScheduleType]:
        try:
            fields = extract_fields(info)
            column_dict = get_schedule_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            schedules = result.mappings().all()
            return [ScheduleType(**schedule) for schedule in schedules]  # type: ignore
        except Exception as e:
            raise e
