from __future__ import annotations
from re import A
from app.core.context import Context
from sqlalchemy import select
import strawberry
from datetime import datetime
import enum
from typing import TYPE_CHECKING, Annotated, Optional

from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.class_model import ClassModel
from app.models.user_model import UserModel

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
    async def user(
        self, info: strawberry.Info[Context]
    ) -> Annotated[
        "UserType", strawberry.lazy("app.graphql.types.user_type")
    ]:
        from app.graphql.types.user_type import UserType
        db = info.context.db
        stmt = select(UserModel).where(UserModel.id == self.user_id)
        result = await db.execute(stmt)
        content = result.scalars().first()
        if content is None:
            raise Exception("Announcement content not found")
        return UserType(
            id=content.id,
            username=content.username,
            email=content.email,
            avatar_url=content.avatar_url,
            class_id=content.class_id,
            password=content.password,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )

    @strawberry.field
    async def class_model(
        self, info: strawberry.Info[Context]
    ) -> Annotated[
        "ClassType", strawberry.lazy("app.graphql.types.class_type")
    ]:
        from app.graphql.types.class_type import ClassType
        db = info.context.db
        stmt = select(ClassModel).where(ClassModel.id == self.class_id)
        result = await db.execute(stmt)
        class_instance = result.scalars().first()
        if class_instance is None:
            raise Exception("Class not found")
        return ClassType(
            id=class_instance.id,
            generation=class_instance.generation,
            group_name=class_instance.group_name,
            major=class_instance.major,
            speciality=class_instance.speciality,
            created_at=class_instance.created_at,
            updated_at=class_instance.updated_at,
        )

    @strawberry.field
    async def content(self, info: strawberry.Info[Context]) -> Annotated[
        "AnnouncementContentType",
        strawberry.lazy(
            "app.graphql.types.announcement_content_type"
        ),
    ]:
        from app.graphql.types.announcement_content_type import AnnouncementContentType
        db = info.context.db
        stmt = select(AnnouncementContentModel).where(
            AnnouncementContentModel.announcement_id == self.id
        )
        result = await db.execute(stmt)
        content = result.scalars().first()
        if content is None:
            raise Exception("Announcement content not found")
        return AnnouncementContentType(
            id=content.id,
            announcement_id=content.announcement_id,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )
