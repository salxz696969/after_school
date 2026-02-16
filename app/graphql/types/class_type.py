from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .assignment_type import AssignmentType
    from .schedule_type import ScheduleType
    from .subject_type import SubjectType
    from .user_type import UserType
    from .announcement_type import AnnouncementType


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
    def users(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "UserType",
            strawberry.lazy("app.graphql.types.user_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.class_loader.user_loader:  # type: ignore
            info.context.class_loader.create_user_loader(fields)  # type: ignore
        return info.context.class_loader.user_loader.load(self.id)  # type: ignore

    @strawberry.field
    def subjects(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "SubjectType",
            strawberry.lazy("app.graphql.types.subject_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.class_loader.subject_loader:  # type: ignore
            info.context.class_loader.create_subject_loader(fields)  # type: ignore
        return info.context.class_loader.subject_loader.load(self.id)  # type: ignore

    @strawberry.field
    def assignments(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentType",
            strawberry.lazy("app.graphql.types.assignment_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.class_loader.assignment_loader:  # type: ignore
            info.context.class_loader.create_assignment_loader(fields)  # type: ignore
        return info.context.class_loader.assignment_loader.load(self.id)  # type: ignore

    @strawberry.field
    def schedules(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ScheduleType",
            strawberry.lazy("app.graphql.types.schedule_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.class_loader.schedule_loader:  # type: ignore
            info.context.class_loader.create_schedule_loader(fields)  # type: ignore
        return info.context.class_loader.schedule_loader.load(self.id)  # type: ignore

    @strawberry.field
    def announcements(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AnnouncementType",
            strawberry.lazy("app.graphql.types.announcement_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.class_loader.announcement_loader:  # type: ignore
            info.context.class_loader.create_announcement_loader(fields)  # type: ignore
        return info.context.class_loader.announcement_loader.load(self.id)  # type: ignore
