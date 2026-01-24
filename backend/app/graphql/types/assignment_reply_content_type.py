from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from sqlalchemy import select
from typing import TYPE_CHECKING, Annotated, List

from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.media_model import MediaModel

if TYPE_CHECKING:
    from .assignment_reply_type import AssignmentReplyType
    from .media_type import MediaType


@strawberry.type
class AssignmentReplyContentType:
    id: int
    assignment_reply_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def assignment_reply(
        self, info: strawberry.Info[Context]
    ) -> Annotated[
        "AssignmentReplyType",
        strawberry.lazy("app.graphql.types.assignment_reply_type"),
    ]:
        from app.graphql.types.assignment_reply_type import AssignmentReplyType
        db = info.context.db
        stmt = select(AssignmentReplyModel).where(
            AssignmentReplyModel.id == self.assignment_reply_id
        )
        result = await db.execute(stmt)
        assignment_reply = result.scalars().first()
        if assignment_reply is None:
            raise Exception("Assignment Reply not found")
        return AssignmentReplyType(
            id=assignment_reply.id,
            assignment_id=assignment_reply.assignment_id,
            user_id=assignment_reply.user_id,
            down_vote=assignment_reply.down_vote,
            up_vote=assignment_reply.up_vote,
            created_at=assignment_reply.created_at,
            updated_at=assignment_reply.updated_at,
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
        stmt = select(MediaModel).where(
            MediaModel.assignment_reply_content_id == self.id
        )
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
