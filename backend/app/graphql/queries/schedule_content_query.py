from __future__ import annotations
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields
from app.utils.get_column import get_schedule_content_columns
from app.core.context import Context
from app.graphql.types.schedule_content_type import ScheduleContentType

@strawberry.type
class ScheduleContentQuery:
    @strawberry.field
    async def get_schedule_contents(self, info: strawberry.Info[Context]) -> List[ScheduleContentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_schedule_content_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            schedule_contents = result.mappings().all()
            return [ScheduleContentType(**schedule_content) for schedule_content in schedule_contents]  # type: ignore
        except Exception as e:
            raise e