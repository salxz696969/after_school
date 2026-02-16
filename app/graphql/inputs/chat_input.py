from __future__ import annotations
from typing import Optional
import strawberry


@strawberry.input
class CreateChatInput:
    chat_room_id: Optional[int] = None
    user_id: Optional[int] = None


@strawberry.input
class UpdateChatInput:
    id: int


@strawberry.input
class DeleteChatInput:
    id: int
