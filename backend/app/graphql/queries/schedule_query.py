from __future__ import annotations
import strawberry


@strawberry.type
class ScheduleQuery:
    @strawberry.field
    def get_schedules(self) -> str:
        return "Getting all schedules"
