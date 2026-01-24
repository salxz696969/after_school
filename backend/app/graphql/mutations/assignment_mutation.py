from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentMutation:
    @strawberry.field
    def create_assignment(self) -> str:
        return "Creating new assignment"
