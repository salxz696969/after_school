from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional
from sqlalchemy import select
from app.core.context import Context
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from app.models.user_model import UserModel

if TYPE_CHECKING:
    from .assignment_type import AssignmentType
    from .user_type import UserType
    from .assignment_reply_content_type import AssignmentReplyContentType


@strawberry.type
class AssignmentReplyType:
    id: int
    assignment_id: int | None = None
    user_id: int | None = None
    up_vote: int | None = None
    down_vote: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def assignment(self, info: strawberry.Info[Context]) -> AssignmentType:
        db = info.context.db
        stmt = select(AssignmentModel).where(AssignmentModel.id == self.assignment_id)
        result = await db.execute(stmt)
        assignment = result.scalars().first()
        if assignment is None:
            raise Exception("Assignment not found")
        return AssignmentType(
            id=assignment.id,
            subject_id=assignment.subject_id,
            class_id=assignment.class_id,
            user_id=assignment.user_id,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at,
        )

    @strawberry.field
    async def user(self, info: strawberry.Info[Context]) -> UserType:
        db = info.context.db
        stmt = select(UserModel).where(UserModel.id == self.user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user is None:
            raise Exception("User not found")
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar_url=user.avatar_url,
            class_id=user.class_id,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @strawberry.field
    async def content(
        self, info: strawberry.Info[Context]
    ) -> AssignmentReplyContentType:
        db = info.context.db
        stmt = select(AssignmentReplyContentModel).where(
            AssignmentReplyContentModel.assignment_reply_id == self.id
        )
        result = await db.execute(stmt)
        content = result.scalars().first()
        if content is None:
            raise Exception("Assignment Reply Content not found")
        return AssignmentReplyContentType(
            id=content.id,
            assignment_reply_id=content.assignment_reply_id,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )
