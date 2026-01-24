from __future__ import annotations
import strawberry


@strawberry.type
class UserQuery:
    @strawberry.field
    def get_users(self) -> str:
        return "Getting all users"
