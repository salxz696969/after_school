from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
import strawberry
from datetime import datetime
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .class_type import ClassType
    from .schedule_content_type import ScheduleContentType


@strawberry.type
class ScheduleType:
    id: int
    class_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def class_(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.schedule_loader.class_loader:  # type: ignore
            info.context.schedule_loader.create_class_loader(fields)  # type: ignore
        return info.context.schedule_loader.class_loader.load(self.id)  # type: ignore

    @strawberry.field
    def schedule_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ScheduleContentType",
        strawberry.lazy("app.graphql.types.schedule_content_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.schedule_loader.content_loader:  # type: ignore
            info.context.schedule_loader.create_content_loader(fields)  # type: ignore
        return info.context.schedule_loader.content_loader.load(self.id)  # type: ignore
