from __future__ import annotations
from typing import TYPE_CHECKING
from strawberry.types import Info
import strawberry
from app.core.context import Context
from app.models.class_model import ClassModel
from app.graphql.types.class_type import ClassType


@strawberry.type
class ClassMutation:
    @strawberry.field
    async def create_class(self, info: Info[Context]) -> ClassType:
        db = info.context.db
        new_class = ClassModel(
            speciality="Computer Science",
            major="Software Engineering",
            group_name="SE-G4",
            generation="2024",
        )
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        return ClassType(
            id=new_class.id,
            speciality=new_class.speciality,
            major=new_class.major,
            group_name=new_class.group_name,
            generation=new_class.generation,
            created_at=new_class.created_at,
            updated_at=new_class.updated_at,
        )

    @strawberry.field
    def ping_class(self, info: Info[Context]) -> str:
        return "Pong from ClassMutation!"
