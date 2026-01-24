from __future__ import annotations
import strawberry


@strawberry.type
class ChatRoomMemberMutation:
    @strawberry.field
    def add_chat_room_member(self) -> str:
        return "Adding chat room member"
