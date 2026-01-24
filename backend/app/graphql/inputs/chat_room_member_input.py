from __future__ import annotations
import strawberry


@strawberry.input
class CreateChatRoomMemberInput:
    chat_room_id: int
    user_id: int

@strawberry.input
class DeleteChatRoomMemberInput:
    chat_room_id: int
    user_id: int