from __future__ import annotations
import strawberry


@strawberry.input
class CreateClassInput:
    speciality: str
    major: str
    group_name: str
    generation: str

@strawberry.input
class UpdateClassInput:
    id: int
    speciality: str
    major: str
    group_name: str
    generation: str

@strawberry.input
class DeleteClassInput:
    id: int