from __future__ import annotations
import strawberry


@strawberry.type
class AssignmentContentMutation:
    @strawberry.field
    def edit_assignment_content(self) -> str:
        return "Editing assignment content"
