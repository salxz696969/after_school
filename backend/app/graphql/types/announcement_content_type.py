from __future__ import annotations
from sqlalchemy import select
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from app.core.context import Context
from app.graphql.types.announcement_type import AnnouncementTypeEnum
from app.models.announcement_model import AnnouncementModel
from app.models.media_model import MediaModel

if TYPE_CHECKING:
    from .announcement_type import AnnouncementType
    from .media_type import MediaType


@strawberry.type
class AnnouncementContentType:
    id: int
    announcement_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def announcement(self, info: strawberry.Info[Context]) -> AnnouncementType:
        db = info.context.db
        stmt = select(AnnouncementModel).where(
            AnnouncementModel.id == self.announcement_id
        )
        result = await db.execute(stmt)
        announcement = result.scalars().first()
        if announcement is None:
            raise Exception("Announcement not found")
        return AnnouncementType(
            id=announcement.id,
            user_id=announcement.user_id,
            class_id=announcement.class_id,
            type=AnnouncementTypeEnum[announcement.type],
            created_at=announcement.created_at,
            updated_at=announcement.updated_at,
        )

    @strawberry.field
    async def medias(self, info: strawberry.Info[Context]) -> List[MediaType]:
        db = info.context.db
        stmt = select(MediaModel).where(MediaModel.announcement_content_id == self.id)
        result = await db.execute(stmt)
        medias = result.scalars().all()
        return [
            MediaType(
                id=media.id,
                announcement_content_id=media.announcement_content_id,
                assignment_content_id=media.assignment_content_id,
                schedule_content_id=media.schedule_content_id,
                chat_content_id=media.chat_content_id,
                assignment_reply_content_id=media.assignment_reply_content_id,
                url=media.url,
                created_at=media.created_at,
                updated_at=media.updated_at,
            )
            for media in medias
        ]
