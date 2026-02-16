from __future__ import annotations
import strawberry


@strawberry.input
class CreateSubjectInput:
    class_id: int
    name: str

@strawberry.input
class UpdateSubjectInput:
    id: int
    name: str

@strawberry.input
class DeleteSubjectInput:
    id: int