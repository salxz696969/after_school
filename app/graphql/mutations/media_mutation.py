from __future__ import annotations
import strawberry


@strawberry.type
class MediaMutation:
    @strawberry.field
    def upload_media(self) -> str:
        return "Uploading media file"
