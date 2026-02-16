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
        fields = extract_fields(info)
        if not info.context.assignment_content_loader.assignment_loader:  # type: ignore
            info.context.assignment_content_loader.create_assignment_loader(fields)  # type: ignore
        return info.context.assignment_content_loader.assignment_loader.load(self.id)  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.assignment_content_loader.media_loader:  # type: ignore
            info.context.assignment_content_loader.create_media_loader(fields)  # type: ignore
        return info.context.assignment_content_loader.media_loader.load(self.id)  # type: ignore
