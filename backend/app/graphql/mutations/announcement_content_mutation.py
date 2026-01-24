from __future__ import annotations
import strawberry


@strawberry.type
class AnnouncementContentMutation:
    @strawberry.field
    def update_announcement_content(self) -> str:
        return "Updating announcement content"
