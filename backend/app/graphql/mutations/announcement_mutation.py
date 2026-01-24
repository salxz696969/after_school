from __future__ import annotations
import strawberry


@strawberry.type
class AnnouncementMutation:
    @strawberry.field
    def create_announcement(self) -> str:
        return "Creating new announcement"
