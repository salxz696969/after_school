from __future__ import annotations
import strawberry


@strawberry.type
class ChatContentMutation:
    @strawberry.field
    def update_chat_content(self) -> str:
        return "Updating chat content"
