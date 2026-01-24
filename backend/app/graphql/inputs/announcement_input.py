from __future__ import annotations
from typing import Optional
import strawberry
from app.graphql.types.announcement_type import AnnouncementTypeEnum


@strawberry.input
class CreateAnnouncementInput:
    user_id: Optional[int] = None
    class_id: Optional[int] = None
    type: AnnouncementTypeEnum


@strawberry.input
class UpdateAnnouncementInput:
    id: int
    type: Optional[AnnouncementTypeEnum] = None


@strawberry.input
class DeleteAnnouncementInput:
    id: int
