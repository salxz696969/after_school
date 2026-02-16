from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from typing import TYPE_CHECKING, Annotated, List

from app.utils import extract_fields

if TYPE_CHECKING:
    from .assignment_reply_type import AssignmentReplyType
    from .media_type import MediaType


@strawberry.type
class AssignmentReplyContentType:
    id: int
    text: str | None = None
    assignment_reply_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def assignment_reply(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentReplyType",
        strawberry.lazy("app.graphql.types.assignment_reply_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_reply_content_loader.assignment_reply_loader:  # type: ignore
            info.context.assignment_reply_content_loader.create_assignment_reply_loader(fields)  # type: ignore
        return info.context.assignment_reply_content_loader.assignment_reply_loader.load(self.id)  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_reply_content_loader.media_loader:  # type: ignore
            info.context.assignment_reply_content_loader.create_media_loader(fields)  # type: ignore
        return info.context.assignment_reply_content_loader.media_loader.load(self.id)  # type: ignore
