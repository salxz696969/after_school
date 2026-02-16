from __future__ import annotations
import strawberry
from typing import Optional


@strawberry.input
class CreateAssignmentReplyContentInput:
    assignment_reply_id: Optional[int] = None
    text: Optional[str] = None


@strawberry.input
class UpdateAssignmentReplyContentInput:
    id: int
    text: Optional[str] = None


@strawberry.input
class DeleteAssignmentReplyContentInput:
    id: int
