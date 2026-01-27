from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
import strawberry
from datetime import datetime
from sqlalchemy import select
from app.core.context import Context
from app.models.class_model import ClassModel
from app.models.schedule_content_model import ScheduleContentModel

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
    async def class_model(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
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
        "ScheduleContentType",
        strawberry.lazy("app.graphql.types.schedule_content_type"),
    ]:
        from app.graphql.types.schedule_content_type import ScheduleContentType
        db = info.context.db
        stmt = select(ScheduleContentModel).where(
            ScheduleContentModel.schedule_id == self.id
        )
        result = await db.execute(stmt)
        content = result.scalars().first()
        if content is None:
            raise Exception("Schedule content not found")
        return ScheduleContentType(
            id=content.id,
            schedule_id=content.schedule_id,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )
