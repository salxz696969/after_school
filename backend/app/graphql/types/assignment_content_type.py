from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from typing import TYPE_CHECKING, Annotated, List

from app.utils import extract_fields

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
    def assignment(self, info: strawberry.Info[Context]) -> Annotated[
        "AssignmentType",
        strawberry.lazy("app.graphql.types.assignment_type"),
    ]:
        fields = extract_fields
        return info.context.assignment_content_loader.assignment_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.assignment_content_loader.media_loader.load((self.id, tuple(fields)))  # type: ignore
