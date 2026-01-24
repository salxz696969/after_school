from __future__ import annotations
import strawberry


@strawberry.type
class ScheduleContentMutation:
    @strawberry.field
    def update_schedule_content(self) -> str:
        return "Updating schedule content"
