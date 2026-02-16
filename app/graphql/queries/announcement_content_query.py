from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy.future import select
from app.core.context import Context
from app.graphql.types.announcement_content_type import AnnouncementContentType
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter


@strawberry.type
class AnnouncementContentQuery:
    @strawberry.field
    async def get_announcement_contents(
        self, info: strawberry.Info[Context]
    ) -> List[AnnouncementContentType]:
        try:
            if not validate_fields(info, "announcementContent"):
                raise HTTPException(status_code=400, detail="Recursive in announcementContent detected. Please remove it from your query.")
            fields = extract_fields(info)
            column_list = ColumnGetter.get_announcement_content_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AnnouncementContentType(**content) for content in contents]  # type: ignore
        except HTTPException:
            raise
        except Exception as e:
            logging.exception(f"Error fetching announcement contents: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch announcement contents")