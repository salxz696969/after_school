from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateScheduleContentInput:
    schedule_id: Optional[int] = None
    text: Optional[str] = None


@strawberry.input
class UpdateScheduleContentInput:
    id: int
    text: Optional[str] = None


@strawberry.input
class DeleteScheduleContentInput:
    id: int
