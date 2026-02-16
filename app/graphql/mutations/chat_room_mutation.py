from __future__ import annotations
import strawberry


@strawberry.type
class ChatRoomMutation:
    @strawberry.field
    def create_chat_room(self) -> str:
        return "Creating new chat room"
