from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateAnnouncementContentInput:
    announcement_id: Optional[int] = None
    text: Optional[str] = None


@strawberry.input
class UpdateAnnouncementContentInput:
    id: int
    text: Optional[str] = None


@strawberry.input
class DeleteAnnouncementContentInput:
    id: int
