from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentReplyContentMutation:
    @strawberry.field
    def modify_reply_content(self) -> str:
        return "Modifying reply content"
