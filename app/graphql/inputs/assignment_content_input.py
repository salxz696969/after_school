from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateAssignmentContentInput:
    assignment_id: Optional[int] = None
    text: Optional[str] = None


@strawberry.input
class UpdateAssignmentContentInput:
    id: int
    text: Optional[str] = None


@strawberry.input
class DeleteAssignmentContentInput:
    id: int
