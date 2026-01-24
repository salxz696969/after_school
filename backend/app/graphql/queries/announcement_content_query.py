from __future__ import annotations
import strawberry


@strawberry.type
class AnnouncementContentQuery:
    @strawberry.field
    def get_announcement_contents(self) -> str:
        return "Getting announcement contents"
