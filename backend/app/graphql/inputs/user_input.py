from __future__ import annotations
import strawberry


@strawberry.input
class CreateUserInput:
    username: str
    email: str
    password: str
    avatar_url: str
    class_id: int

@strawberry.input
class UpdateUserInput:
    id: int
    username: str
    email: str
    avatar_url: str
    class_id: int

@strawberry.input
class DeleteUserInput:
    id: int