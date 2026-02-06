from __future__ import annotations
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields
from app.utils.get_column import get_media_columns
from app.core.context import Context
from app.graphql.types.media_type import MediaType

@strawberry.type
class MediaQuery:
    @strawberry.field
    async def get_medias(self, info: strawberry.Info[Context]) -> List[MediaType]:
        try:
            fields = extract_fields(info)
            column_dict = get_media_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            medias = result.mappings().all()
            return [MediaType(**media) for media in medias]  # type: ignore
        except Exception as e:
            raise e