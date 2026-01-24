from __future__ import annotations
import strawberry


@strawberry.type
class ChatRoomMemberQuery:
    @strawberry.field
    def get_chat_room_members(self) -> str:
        return "Getting chat room members"
