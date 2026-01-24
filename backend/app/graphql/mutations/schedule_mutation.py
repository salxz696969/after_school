from __future__ import annotations
import strawberry


@strawberry.type
class ScheduleMutation:
    @strawberry.field
    def create_schedule(self) -> str:
        return "Creating new schedule"
