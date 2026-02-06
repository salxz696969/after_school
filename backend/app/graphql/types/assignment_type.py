from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .user_type import UserType
    from .subject_type import SubjectType
    from .class_type import ClassType
    from .assignment_reply_type import AssignmentReplyType
    from .assignment_content_type import AssignmentContentType


@strawberry.type
class AssignmentType:
    id: int
    user_id: int | None = None
    subject_id: int | None = None
    class_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def user(self, info: strawberry.Info[Context]) -> Annotated[
        "UserType",
        strawberry.lazy("app.graphql.types.user_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_loader.user_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def subject(self, info: strawberry.Info[Context]) -> Annotated[
        "SubjectType",
        strawberry.lazy("app.graphql.types.subject_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_loader.subject_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def class_model(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_loader.class_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def replies(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentReplyType",
            strawberry.lazy("app.graphql.types.assignment_reply_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.assignment_loader.replies_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def content(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentContentType",
        strawberry.lazy("app.graphql.types.assignment_content_type"),
    ]:
        fields = extract_fields(info)
        return info.context.assignment_loader.content_loader.load((self.id, tuple(fields)))  # type: ignore
