from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .schedule_type import ScheduleType
    from .media_type import MediaType


@strawberry.type
class ScheduleContentType:
    id: int
    text: str | None = None
    schedule_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def schedule(self, info: strawberry.Info[Context]) -> Annotated[
        "ScheduleType",
        strawberry.lazy("app.graphql.types.schedule_type"),
    ]:
        fields = extract_fields(info)
        return info.context.schedule_content_loader.schedule_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.schedule_content_loader.media_loader.load((self.id, tuple(fields)))  # type: ignore
