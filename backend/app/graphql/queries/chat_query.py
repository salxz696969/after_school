from __future__ import annotations
import strawberry


@strawberry.type
class ChatQuery:
    @strawberry.field
    def fetch_chats(self) -> str:
        return "Fetching all chats"
