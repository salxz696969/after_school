from __future__ import annotations
import logging
from fastapi import HTTPException
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.media_type import MediaType


@strawberry.type
class MediaQuery:
    @strawberry.field
    async def get_medias(self, info: strawberry.Info[Context]) -> List[MediaType]:
        try:
            if not validate_fields(info, "media"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in media detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_media_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
                return [MediaType(**media) for media in medias]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch medias")
