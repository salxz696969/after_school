from __future__ import annotations
from app.core.context import Context
import strawberry
from datetime import datetime
import enum
from typing import TYPE_CHECKING, Annotated

from app.utils import extract_fields

if TYPE_CHECKING:
    from .class_type import ClassType
    from .user_type import UserType
    from .announcement_content_type import AnnouncementContentType


@strawberry.enum
class AnnouncementTypeEnum(enum.Enum):
    GENERAL = "general"
    LEAKS = "leaks"


@strawberry.type
class AnnouncementType:
    id: int
    user_id: int | None = None
    class_id: int | None = None
    type: AnnouncementTypeEnum | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def user(
        self, info: strawberry.Info[Context]
    ) -> Annotated["UserType", strawberry.lazy("app.graphql.types.user_type")]:
        fields = extract_fields(info)
        if not info.context.announcement_loader.user_loader:  # type: ignore
            info.context.announcement_loader.create_user_loader(fields)  # type: ignore
        return info.context.announcement_loader.user_loader.load(self.id)  # type: ignore

    @strawberry.field
    def class_(
        self, info: strawberry.Info[Context]
    ) -> Annotated["ClassType", strawberry.lazy("app.graphql.types.class_type")]:
        fields = extract_fields(info)
        if not info.context.announcement_loader.class_loader:  # type: ignore
            info.context.announcement_loader.create_class_loader(fields)  # type: ignore
        return info.context.announcement_loader.class_loader.load(self.id)  # type: ignore

    @strawberry.field
    def content(self, info: strawberry.Info[Context]) -> Annotated[
        "AnnouncementContentType",
        strawberry.lazy("app.graphql.types.announcement_content_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.announcement_loader.announcement_content_loader:  # type: ignore
            info.context.announcement_loader.create_announcement_content_loader(fields)  # type: ignore
        return info.context.announcement_loader.announcement_content_loader.load(self.id)  # type: ignore
