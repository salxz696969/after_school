from __future__ import annotations
from sqlalchemy import select
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from app.core.context import Context
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_model import AssignmentModel
from app.models.schedule_model import ScheduleModel
from app.models.subject_model import SubjectModel
from app.models.user_model import UserModel

if TYPE_CHECKING:
    from .assignment_type import AssignmentType
    from .schedule_type import ScheduleType
    from .subject_type import SubjectType
    from .user_type import UserType
    from .announcement_type import AnnouncementType, AnnouncementTypeEnum


@strawberry.type
class ClassType:
    id: int
    speciality: str | None = None
    major: str | None = None
    group_name: str | None = None
    generation: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def users(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "UserType",
            strawberry.lazy("app.graphql.types.user_type"),
        ]
    ]:
        from app.graphql.types.user_type import UserType
        db = info.context.db
        stmt = select(UserModel).where(UserModel.class_id == self.id)
        result = await db.execute(stmt)
        users = result.scalars().all()
        return [
            UserType(
                id=user.id,
                avatar_url=user.avatar_url,
                class_id=user.class_id,
                email=user.email,
                password=user.password,
                username=user.username,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    @strawberry.field
    async def subjects(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "SubjectType",
            strawberry.lazy("app.graphql.types.subject_type"),
        ]
    ]:
        from app.graphql.types.subject_type import SubjectType
        db = info.context.db
        stmt = select(SubjectModel).where(SubjectModel.class_id == self.id)
        result = await db.execute(stmt)
        subjects = result.scalars().all()
        return [
            SubjectType(
                id=subject.id,
                class_id=subject.class_id,
                name=subject.name,
                created_at=subject.created_at,
                updated_at=subject.updated_at,
            )
            for subject in subjects
        ]

    @strawberry.field
    async def assignments(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentType",
            strawberry.lazy("app.graphql.types.assignment_type"),
        ]
    ]:
        from app.graphql.types.assignment_type import AssignmentType
        db = info.context.db
        stmt = select(AssignmentModel).where(AssignmentModel.class_id == self.id)
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        return [
            AssignmentType(
                id=assignment.id,
                class_id=assignment.class_id,
                subject_id=assignment.subject_id,
                user_id=assignment.user_id,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at,
            )
            for assignment in assignments
        ]

    @strawberry.field
    async def schedules(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ScheduleType",
            strawberry.lazy("app.graphql.types.schedule_type"),
        ]
    ]:
        from app.graphql.types.schedule_type import ScheduleType
        db = info.context.db
        stmt = select(ScheduleModel).where(ScheduleModel.class_id == self.id)
        result = await db.execute(stmt)
        schedules = result.scalars().all()
        return [
            ScheduleType(
                id=schedule.id,
                class_id=schedule.class_id,
                created_at=schedule.created_at,
                updated_at=schedule.updated_at,
            )
            for schedule in schedules
        ]

    @strawberry.field
    async def announcements(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AnnouncementType",
            strawberry.lazy("app.graphql.types.announcement_type"),
        ]
    ]:
        from app.graphql.types.announcement_type import AnnouncementType
        db = info.context.db
        stmt = select(AnnouncementModel).where(AnnouncementModel.class_id == self.id)
        result = await db.execute(stmt)
        announcements = result.scalars().all()
        return [
            AnnouncementType(
                id=announcement.id,
                class_id=announcement.class_id,
                type=AnnouncementTypeEnum[announcement.type],
                user_id=announcement.user_id,
                created_at=announcement.created_at,
                updated_at=announcement.updated_at,
            )
            for announcement in announcements
        ]
