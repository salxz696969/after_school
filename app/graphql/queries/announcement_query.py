from __future__ import annotations
import logging
from fastapi import HTTPException
import strawberry
from typing import List
from app.core.context import Context
from sqlalchemy import select
from app.graphql.types.announcement_type import AnnouncementType
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter


@strawberry.type
class AnnouncementQuery:
    @strawberry.field
    async def get_announcements(
        self, info: strawberry.Info[Context]
    ) -> List[AnnouncementType]:
        try:
            if not validate_fields(info, "announcement"):
                raise HTTPException(status_code=400, detail="Recursive in announcement detected. Please remove it from your query.")
            fields = extract_fields(info)
            column_list = ColumnGetter.get_announcement_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                announcements = result.mappings().all()  # type: ignore
                return [AnnouncementType(**announcement) for announcement in announcements]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching announcements: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch announcements")
