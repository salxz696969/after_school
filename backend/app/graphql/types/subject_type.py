from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .class_type import ClassType
    from .assignment_type import AssignmentType


@strawberry.type
class SubjectType:
    id: int
    class_id: int | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def class_model(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
        fields = extract_fields(info)
        return info.context.subject_loader.class_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def assignments(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentType",
            strawberry.lazy("app.graphql.types.assignment_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.subject_loader.assignment_loader.load((self.id, tuple(fields)))  # type: ignore
