from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from sqlalchemy import select
from typing import TYPE_CHECKING, Annotated, List

from app.models.assignment_model import AssignmentModel
from app.models.media_model import MediaModel

if TYPE_CHECKING:
    from .assignment_type import AssignmentType
    from .media_type import MediaType


@strawberry.type
class AssignmentContentType:
    id: int
    assignment_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def assignment(self, info: strawberry.Info[Context]) -> AssignmentType:
        db = info.context.db
        stmt = select(AssignmentModel).where(AssignmentModel.id == self.assignment_id)
        result = await db.execute(stmt)
        assignment = result.scalars().first()
        if assignment is None:
            raise Exception("Assignment not found")
        return AssignmentType(
            id=assignment.id,
            subject_id=assignment.subject_id,
            class_id=assignment.class_id,
            user_id=assignment.user_id,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at,
        )

    @strawberry.field
    async def medias(self, info: strawberry.Info[Context]) -> List[MediaType]:
        db = info.context.db
        stmt = select(MediaModel).where(MediaModel.assignment_content_id == self.id)
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
