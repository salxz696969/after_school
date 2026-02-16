from __future__ import annotations
import strawberry


@strawberry.type
class UserMutation:
    @strawberry.field
    def register_user(self) -> str:
        return "Registering new user"
