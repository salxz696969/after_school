from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateAssignmentInput:
    user_id: Optional[int] = None
    subject_id: Optional[int] = None
    class_id: Optional[int] = None


@strawberry.input
class UpdateAssignmentInput:
    id: int


@strawberry.input
class DeleteAssignmentInput:
    id: int
