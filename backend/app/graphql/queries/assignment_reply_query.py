from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentReplyQuery:
    @strawberry.field
    def view_assignment_replies(self) -> str:
        return "Viewing assignment replies"
