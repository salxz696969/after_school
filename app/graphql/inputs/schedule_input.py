from __future__ import annotations
from typing import Optional
import strawberry


@strawberry.input
class ScheduleInput:
    class_id: Optional[int] = None


@strawberry.input
class UpdateScheduleInput:
    id: int


@strawberry.input
class DeleteScheduleInput:
    id: int
