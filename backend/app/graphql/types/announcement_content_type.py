from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .announcement_type import AnnouncementType
    from .media_type import MediaType


@strawberry.type
class AnnouncementContentType:
    id: int
    text: str | None = None
    announcement_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def announcement(self, info: strawberry.Info[Context]) -> Annotated[
        "AnnouncementType",
        strawberry.lazy("app.graphql.types.announcement_type"),
    ]:

        fields = extract_fields(info)
        return info.context.announcement_content_loader.announcement_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:

        fields = extract_fields(info)
        return info.context.announcement_content_loader.media_loader.load((self.id, tuple(fields)))  # type: ignore
