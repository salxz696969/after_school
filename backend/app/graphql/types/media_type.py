from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional
from app.core.context import Context
from app.models.chat_content_model import ChatContentModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.assignment_content_model import AssignmentContentModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from sqlalchemy import select

if TYPE_CHECKING:
    from .chat_content_type import ChatContentType
    from .schedule_content_type import ScheduleContentType
    from .announcement_content_type import AnnouncementContentType
    from .assignment_content_type import AssignmentContentType
    from .assignment_reply_content_type import AssignmentReplyContentType


@strawberry.type
class MediaType:
    id: int
    url: str | None = None
    chat_content_id: int | None = None
    schedule_content_id: int | None = None
    announcement_content_id: int | None = None
    assignment_content_id: int | None = None
    assignment_reply_content_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def chat_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatContentType",
        strawberry.lazy("app.graphql.types.chat_content_type"),
    ]:
        from app.graphql.types.chat_content_type import ChatContentType
        db = info.context.db
        stmt = select(ChatContentModel).where(
            ChatContentModel.id == self.chat_content_id
        )
        result = await db.execute(stmt)
        chat_content = result.scalars().first()
        if chat_content is None:
            raise Exception("Chat Content not found")
        return ChatContentType(
            id=chat_content.id,
            chat_id=chat_content.chat_id,
            created_at=chat_content.created_at,
            updated_at=chat_content.updated_at,
        )

    @strawberry.field
    async def schedule_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ScheduleContentType",
        strawberry.lazy("app.graphql.types.schedule_content_type"),
    ]:
        from app.graphql.types.schedule_content_type import ScheduleContentType
        db = info.context.db
        stmt = select(ScheduleContentModel).where(
            ScheduleContentModel.id == self.schedule_content_id
        )
        result = await db.execute(stmt)
        schedule_content = result.scalars().first()
        if schedule_content is None:
            raise Exception("Schedule Content not found")
        return ScheduleContentType(
            id=schedule_content.id,
            schedule_id=schedule_content.schedule_id,
            created_at=schedule_content.created_at,
            updated_at=schedule_content.updated_at,
        )

    @strawberry.field
    async def announcement_content(self, info: strawberry.Info[Context]) -> Annotated[
        "AnnouncementContentType",
        strawberry.lazy(
            "app.graphql.types.announcement_content_type"
        ),
    ]:
        from app.graphql.types.announcement_content_type import AnnouncementContentType
        db = info.context.db
        stmt = select(AnnouncementContentModel).where(
            AnnouncementContentModel.id == self.announcement_content_id
        )
        result = await db.execute(stmt)
        announcement_content = result.scalars().first()
        if announcement_content is None:
            raise Exception("Announcement Content not found")
        return AnnouncementContentType(
            id=announcement_content.id,
            announcement_id=announcement_content.announcement_id,
            created_at=announcement_content.created_at,
            updated_at=announcement_content.updated_at,
        )

    @strawberry.field
    async def assignment_content(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentContentType",
        strawberry.lazy(
            "app.graphql.types.assignment_content_type"
        ),
    ]:
        from app.graphql.types.assignment_content_type import AssignmentContentType
        db = info.context.db
        stmt = select(AssignmentContentModel).where(
            AssignmentContentModel.id == self.assignment_content_id
        )
        result = await db.execute(stmt)
        assignment_content = result.scalars().first()
        if assignment_content is None:
            raise Exception("Assignment Content not found")
        return AssignmentContentType(
            id=assignment_content.id,
            assignment_id=assignment_content.assignment_id,
            created_at=assignment_content.created_at,
            updated_at=assignment_content.updated_at,
        )

    @strawberry.field
    async def assignment_reply_content(
        self, info: strawberry.Info[Context]
    ) -> Annotated[
        "AssignmentReplyContentType",
        strawberry.lazy(
            "app.graphql.types.assignment_reply_content_type"
        ),
    ]:
        from app.graphql.types.assignment_reply_content_type import AssignmentReplyContentType
        db = info.context.db
        stmt = select(AssignmentReplyContentModel).where(
            AssignmentReplyContentModel.id == self.assignment_reply_content_id
        )
        result = await db.execute(stmt)
        assignment_reply_content = result.scalars().first()
        if assignment_reply_content is None:
            raise Exception("Assignment Reply Content not found")
        return AssignmentReplyContentType(
            id=assignment_reply_content.id,
            assignment_reply_id=assignment_reply_content.assignment_reply_id,
            created_at=assignment_reply_content.created_at,
            updated_at=assignment_reply_content.updated_at,
        )
