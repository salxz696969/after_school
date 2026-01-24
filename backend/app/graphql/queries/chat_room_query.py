from __future__ import annotations
import strawberry


@strawberry.type
class ChatRoomQuery:
    @strawberry.field
    def list_chat_rooms(self) -> str:
        return "Listing chat rooms"
