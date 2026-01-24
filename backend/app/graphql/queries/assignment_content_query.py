from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentContentQuery:
    @strawberry.field
    def fetch_assignment_contents(self) -> str:
        return "Fetching assignment contents"
