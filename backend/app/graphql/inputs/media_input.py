from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateMediaInput:
    url: str
    chat_content_id: Optional[int] = None
    schedule_content_id: Optional[int] = None
    announcement_content_id: Optional[int] = None
    assignment_content_id: Optional[int] = None
    assignment_reply_content_id: Optional[int] = None


@strawberry.input
class UpdateMediaInput:
    id: int
    url: Optional[str] = None


@strawberry.input
class DeleteMediaInput:
    id: int
