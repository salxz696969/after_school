from __future__ import annotations
import strawberry


@strawberry.type
class ChatContentQuery:
    @strawberry.field
    def get_chat_contents(self) -> str:
        return "Getting chat contents"
