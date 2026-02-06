from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated
from app.core.context import Context
from app.utils import extract_fields

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
    def chat_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatContentType",
        strawberry.lazy("app.graphql.types.chat_content_type"),
    ]:
        fields = extract_fields(info)
        return info.context.media_loader.chat_content_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def schedule_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ScheduleContentType",
        strawberry.lazy("app.graphql.types.schedule_content_type"),
    ]:
        fields = extract_fields(info)
        return info.context.media_loader.schedule_content_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def announcement_content(self, info: strawberry.Info[Context]) -> Annotated[
        "AnnouncementContentType",
        strawberry.lazy(
            "app.graphql.types.announcement_content_type"
        ),
    ]:
        fields = extract_fields(info)
        return info.context.media_loader.announcement_content_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def assignment_content(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentContentType",
        strawberry.lazy(
            "app.graphql.types.assignment_content_type"
        ),
    ]:
        fields = extract_fields(info)
        return info.context.media_loader.assignment_content_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def assignment_reply_content(
        self, info: strawberry.Info[Context]
    ) -> Annotated[
        "AssignmentReplyContentType",
        strawberry.lazy(
            "app.graphql.types.assignment_reply_content_type"
        ),
    ]:
        fields = extract_fields(info)
        return info.context.media_loader.assignment_reply_content_loader.load((self.id, tuple(fields)))  # type: ignore
