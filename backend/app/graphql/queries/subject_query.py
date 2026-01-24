from __future__ import annotations
import strawberry


@strawberry.type
class SubjectQuery:
    @strawberry.field
    def view_subjects(self) -> str:
        return "Viewing all subjects"
