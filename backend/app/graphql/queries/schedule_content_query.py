from __future__ import annotations
import strawberry


@strawberry.type
class ScheduleContentQuery:
    @strawberry.field
    def retrieve_schedule_content(self) -> str:
        return "Retrieving schedule content"
