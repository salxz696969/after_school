from __future__ import annotations
import strawberry
from app.graphql.types.chat_room_type import ChatRoomTypeEnum


@strawberry.input
class CreateChatRoomInput:
    chat_room_type: ChatRoomTypeEnum
    chat_room_name: str
    avatar_url: str

@strawberry.input
class UpdateChatRoomInput:
    id: int
    chat_room_name: str
    avatar_url: str

@strawberry.input
class DeleteChatRoomInput:
    id: int