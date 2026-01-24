from __future__ import annotations
import strawberry


@strawberry.type
class MediaQuery:
    @strawberry.field
    def fetch_media(self) -> str:
        return "Fetching media files"
