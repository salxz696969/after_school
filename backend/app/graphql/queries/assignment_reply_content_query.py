from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentReplyContentQuery:
    @strawberry.field
    def get_reply_content(self) -> str:
        return "Getting reply content"
