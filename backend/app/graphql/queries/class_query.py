from __future__ import annotations
import logging
from sqlalchemy import select
import strawberry
from strawberry.types import Info
from app.core.context import Context
from app.graphql.types.class_type import ClassType
from app.models.class_model import ClassModel
import logging


@strawberry.type
class ClassQuery:

    def _is_valid_field(self, field: list[str]) -> bool:
        valid_fields = {
            "id",
            "speciality",
            "major",
            "group_name",
            "generation",
            "created_at",
            "updated_at",
            "users",
            "subjects",
            "assignments",
            "schedules",
            "announcements",
        }
        for f in field:
            if f not in valid_fields:
                raise ValueError(f"Invalid field: {f}")
        return True

    @strawberry.field
    async def get_class(self, info: Info[Context], class_id: int) -> ClassType:
        db = info.context.db
        stmt = select(ClassModel).where(ClassModel.id == class_id)
        result = await db.execute(stmt)
        class_instance = result.scalars().first()
        if class_instance is None:
            raise ValueError(f"Class with id {class_id} not found")
        return ClassType(
            id=class_instance.id,
            speciality=class_instance.speciality,
            major=class_instance.major,
            group_name=class_instance.group_name,
            generation=class_instance.generation,
            created_at=class_instance.created_at,
            updated_at=class_instance.updated_at,
        )

    @strawberry.field
    async def get_classes(self, info: Info[Context]) -> list[ClassType]:
        try:
            db = info.context.db
            stmt = select(ClassModel)
            result = await db.execute(stmt)
            rows = result.all()

            return [
                ClassType(
                    id=r.ClassModel.id or 0,
                    speciality=r.ClassModel.speciality or "",
                    major=r.ClassModel.major or "",
                    group_name=r.ClassModel.group_name or "",
                    generation=r.ClassModel.generation or "",
                    created_at=r.ClassModel.created_at or None,
                    updated_at=r.ClassModel.updated_at or None,
                )
                for r in rows
            ]
        except Exception as e:
            logging.error(f"Error in get_classes: {e}")
            raise e
