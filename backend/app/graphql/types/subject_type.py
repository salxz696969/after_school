from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List
from sqlalchemy import select
from app.core.context import Context
from app.models.assignment_model import AssignmentModel
from app.models.class_model import ClassModel

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
    async def class_model(self, info: strawberry.Info[Context]) -> ClassType:
        db = info.context.db
        stmt = select(ClassModel).where(ClassModel.id == self.class_id)
        result = await db.execute(stmt)
        class_instance = result.scalars().first()
        if class_instance is None:
            raise Exception("Class not found")
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
    async def assignments(self, info: strawberry.Info[Context]) -> List[AssignmentType]:
        db = info.context.db
        stmt = select(AssignmentModel).where(AssignmentModel.subject_id == self.id)
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        if assignments is None:
            raise Exception("No assignments found")
        return [
            AssignmentType(
                id=assignment.id,
                subject_id=assignment.subject_id,
                class_id=assignment.class_id,
                user_id=assignment.user_id,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at,
            )
            for assignment in assignments
        ]
