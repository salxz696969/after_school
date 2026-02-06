from __future__ import annotations
from typing import List
import strawberry

from app.core.context import Context
from app.graphql.types.announcement_content_type import AnnouncementContentType
from app.utils import extract_fields
from app.utils.get_column import get_announcement_content_columns


@strawberry.type
class AnnouncementContentQuery:
    @strawberry.field
    async def get_announcement_contents(
        self, info: strawberry.Info[Context]
    ) -> List[AnnouncementContentType]:
        try:
            fields = extract_fields(info)
            column_dict = get_announcement_content_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AnnouncementContentType(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
