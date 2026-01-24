from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional, List
from app.core.context import Context
from sqlalchemy import select
from app.models.assignment_content_model import AssignmentContentModel
from app.models.user_model import UserModel
from app.models.subject_model import SubjectModel
from app.models.class_model import ClassModel
from app.models.assignment_reply_model import AssignmentReplyModel

if TYPE_CHECKING:
    from .user_type import UserType
    from .subject_type import SubjectType
    from .class_type import ClassType
    from .assignment_reply_type import AssignmentReplyType
    from .assignment_content_type import AssignmentContentType


@strawberry.type
class AssignmentType:
    id: int
    user_id: int | None = None
    subject_id: int | None = None
    class_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

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
    async def subject(self, info: strawberry.Info[Context]) -> SubjectType:
        db = info.context.db
        stmt = select(SubjectModel).where(SubjectModel.id == self.subject_id)
        result = await db.execute(stmt)
        subject = result.scalars().first()
        if subject is None:
            raise Exception("Subject not found")
        return SubjectType(
            id=subject.id,
            name=subject.name,
            class_id=subject.class_id,
            created_at=subject.created_at,
            updated_at=subject.updated_at,
        )

    @strawberry.field
    async def class_model(self, info: strawberry.Info[Context]) -> ClassType:
        db = info.context.db
        stmt = select(ClassModel).where(ClassModel.id == self.class_id)
        result = await db.execute(stmt)
        class_model = result.scalars().first()
        if class_model is None:
            raise Exception("Class not found")
        return ClassType(
            id=class_model.id,
            speciality=class_model.speciality,
            created_at=class_model.created_at,
            updated_at=class_model.updated_at,
        )

    @strawberry.field
    async def replies(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentReplyType]:
        db = info.context.db
        stmt = select(AssignmentReplyModel).where(
            AssignmentReplyModel.assignment_id == self.id
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        return [
            AssignmentReplyType(
                id=reply.id,
                assignment_id=reply.assignment_id,
                user_id=reply.user_id,
                up_vote=reply.up_vote,
                down_vote=reply.down_vote,
                created_at=reply.created_at,
                updated_at=reply.updated_at,
            )
            for reply in replies
        ]

    @strawberry.field
    async def content(self, info: strawberry.Info[Context]) -> AssignmentContentType:
        db = info.context.db
        stmt = select(AssignmentContentModel).where(
            AssignmentContentModel.assignment_id == self.id
        )
        result = await db.execute(stmt)
        content = result.scalars().first()
        if content is None:
            raise Exception("Assignment content not found")
        return AssignmentContentType(
            id=content.id,
            assignment_id=content.assignment_id,
            created_at=content.created_at,
            updated_at=content.updated_at,
        )
