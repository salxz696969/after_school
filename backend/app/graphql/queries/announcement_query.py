from __future__ import annotations
import strawberry

@strawberry.type
class AnnouncementQuery:
    @strawberry.field
    def get_announcements(self) -> str:
        return "Getting all announcements"