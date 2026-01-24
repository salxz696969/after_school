from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentReplyMutation:
    @strawberry.field
    def submit_assignment_reply(self) -> str:
        return "Submitting assignment reply"
