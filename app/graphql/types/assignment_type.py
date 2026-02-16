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
        if not info.context.assignment_loader.user_loader:  # type: ignore
            info.context.assignment_loader.create_user_loader(fields)  # type: ignore
        return info.context.assignment_loader.user_loader.load(self.id)  # type: ignore

    @strawberry.field
    def subject(self, info: strawberry.Info[Context]) -> Annotated[
        "SubjectType",
        strawberry.lazy("app.graphql.types.subject_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_loader.subject_loader:  # type: ignore
            info.context.assignment_loader.create_subject_loader(fields)  # type: ignore
        return info.context.assignment_loader.subject_loader.load(self.id)  # type: ignore

    @strawberry.field
    def class_(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_loader.class_loader:  # type: ignore
            info.context.assignment_loader.create_class_loader(fields)  # type: ignore
        return info.context.assignment_loader.class_loader.load(self.id)  # type: ignore

    @strawberry.field
    def assignment_replies(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentReplyType",
            strawberry.lazy("app.graphql.types.assignment_reply_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_loader.assignment_reply_loader:  # type: ignore
            info.context.assignment_loader.create_assignment_reply_loader(fields)  # type: ignore
        return info.context.assignment_loader.assignment_reply_loader.load(self.id)  # type: ignore

    @strawberry.field
    def assignment_content(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentContentType",
        strawberry.lazy("app.graphql.types.assignment_content_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_loader.assignment_content_loader:  # type: ignore
            info.context.assignment_loader.create_assignment_content_loader(fields)  # type: ignore
        return info.context.assignment_loader.assignment_content_loader.load(self.id)  # type: ignore
