from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateChatContentInput:
    chat_id: Optional[int] = None
    text: Optional[str] = None


@strawberry.input
class UpdateChatContentInput:
    id: int
    text: Optional[str] = None


@strawberry.input
class DeleteChatContentInput:
    id: int
