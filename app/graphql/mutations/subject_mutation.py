from __future__ import annotations
import strawberry


@strawberry.type
class SubjectMutation:
    @strawberry.field
    def create_subject(self) -> str:
        return "Creating new subject"
