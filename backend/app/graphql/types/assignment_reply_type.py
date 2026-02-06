from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .assignment_type import AssignmentType
    from .user_type import UserType
    from .assignment_reply_content_type import AssignmentReplyContentType


@strawberry.type
class AssignmentReplyType:
    id: int
    assignment_id: int | None = None
    user_id: int | None = None
    up_vote: int | None = None
    down_vote: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def assignment(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentType",
        strawberry.lazy("app.graphql.types.assignment_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_reply_loader.assignment_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def user(self, info: strawberry.Info[Context]) -> Annotated[
        "UserType",
        strawberry.lazy("app.graphql.types.user_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_reply_loader.user_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def content(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentReplyContentType",
        strawberry.lazy("app.graphql.types.assignment_reply_content_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_reply_loader.content_loader.load((self.id, tuple(fields)))  # type: ignore
