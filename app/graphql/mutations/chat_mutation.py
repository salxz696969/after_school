from __future__ import annotations
import strawberry


@strawberry.type
class ChatMutation:
    @strawberry.field
    def send_chat(self) -> str:
        return "Sending new chat"
