from __future__ import annotations
from typing import Optional
import strawberry


@strawberry.input
class CreateAssignmentReplyInput:
    assignment_id: Optional[int] = None
    user_id: Optional[int] = None
    up_vote: int = 0
    down_vote: int = 0


@strawberry.input
class UpdateAssignmentReplyInput:
    id: int
    up_vote: Optional[int] = None
    down_vote: Optional[int] = None


@strawberry.input
class DeleteAssignmentReplyInput:
    id: int
