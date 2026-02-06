from __future__ import annotations
import strawberry
from typing import List
from app.core.context import Context
from sqlalchemy import select
from app.graphql.types.announcement_type import AnnouncementType
from app.utils import extract_fields
from app.utils.get_column import get_announcement_columns

@strawberry.type
class AnnouncementQuery:
    @strawberry.field
    async def get_announcements(self, info: strawberry.Info[Context]) -> List[AnnouncementType]:
        try:
            fields = extract_fields(info)
            column_dict = get_announcement_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            announcements = result.mappings().all()
            return [AnnouncementType(**announcement) for announcement in announcements]  # type: ignore
        except Exception as e:
            raise e