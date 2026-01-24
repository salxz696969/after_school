from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentQuery:
    @strawberry.field
    def list_assignments(self) -> str:
        return "Listing all assignments"
