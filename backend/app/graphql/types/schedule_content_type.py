from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List, Optional
from sqlalchemy import select
from app.core.context import Context
from app.models.schedule_model import ScheduleModel
from app.models.media_model import MediaModel

if TYPE_CHECKING:
    from .schedule_type import ScheduleType
    from .media_type import MediaType


@strawberry.type
class ScheduleContentType:
    id: int
    schedule_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def schedule(self, info: strawberry.Info[Context]) -> Annotated[
        "ScheduleType",
        strawberry.lazy("app.graphql.types.schedule_type"),
    ]:
        from app.graphql.types.schedule_type import ScheduleType
        db = info.context.db
        stmt = select(ScheduleModel).where(ScheduleModel.id == self.schedule_id)
        result = await db.execute(stmt)
        schedule = result.scalars().first()
        if schedule is None:
            raise Exception("Schedule not found")
        return ScheduleType(
            id=schedule.id,
            class_id=schedule.class_id,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )

    @strawberry.field
    async def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        from app.graphql.types.media_type import MediaType
        db = info.context.db
        stmt = select(MediaModel).where(MediaModel.schedule_content_id == self.id)
        result = await db.execute(stmt)
        medias = result.scalars().all()
        return [
            MediaType(
                id=media.id,
                schedule_content_id=media.schedule_content_id,
                url=media.url,
                created_at=media.created_at,
                updated_at=media.updated_at,
            )
            for media in medias
        ]
