from __future__ import annotations
from strawberry.types import Info
import strawberry
from app.core.context import Context

@strawberry.type
class ClassMutation:

    @strawberry.field
    def ping_class(self, info: Info[Context]) -> str:
        return "Pong from ClassMutation!"
