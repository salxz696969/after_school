from __future__ import annotations
import select
from sqlalchemy import select
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List

from app.core.context import Context
from app.graphql.types.announcement_type import AnnouncementTypeEnum
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel
from app.models.class_model import ClassModel

if TYPE_CHECKING:
    from .assignment_reply_type import AssignmentReplyType
    from .assignment_type import AssignmentType
    from .chat_room_member_type import ChatRoomMemberType
    from .chat_type import ChatType
    from .class_type import ClassType
    from .announcement_type import AnnouncementType


@strawberry.type
class UserType:
    id: int
    username: str | None = None
    email: str | None = None
    password: str | None = None
    avatar_url: str | None = None
    class_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def class_(self, info: strawberry.Info[Context]) -> ClassType:
        db = info.context.db
        stmt = select(ClassModel).where(ClassModel.id == self.class_id)
        result = await db.execute(stmt)
        class_instance = result.scalars().first()
        if class_instance is None:
            raise Exception("Class not found")
        return ClassType(
            id=class_instance.id,
            generation=class_instance.generation,
            group_name=class_instance.group_name,
            major=class_instance.major,
            speciality=class_instance.speciality,
            created_at=class_instance.created_at,
            updated_at=class_instance.updated_at,
        )

    @strawberry.field
    async def assignments(self, info: strawberry.Info[Context]) -> List[AssignmentType]:
        db = info.context.db
        stmt = select(AssignmentModel).where(AssignmentModel.user_id == self.id)
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        return [
            AssignmentType(
                id=assignment.id,
                user_id=assignment.user_id,
                subject_id=assignment.subject_id,
                class_id=assignment.class_id,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at,
            )
            for assignment in assignments
        ]

    @strawberry.field
    async def assignment_replies(
        self, info: strawberry.Info[Context]
    ) -> List[AssignmentReplyType]:
        db = info.context.db
        stmt = select(AssignmentReplyModel).where(
            AssignmentReplyModel.user_id == self.id
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        return [
            AssignmentReplyType(
                id=reply.id,
                assignment_id=reply.assignment_id,
                user_id=reply.user_id,
                down_vote=reply.down_vote,
                up_vote=reply.up_vote,
                created_at=reply.created_at,
                updated_at=reply.updated_at,
            )
            for reply in replies
        ]

    @strawberry.field
    async def announcements(
        self, info: strawberry.Info[Context]
    ) -> List[AnnouncementType]:
        db = info.context.db
        stmt = select(AnnouncementModel).where(AnnouncementModel.user_id == self.id)
        result = await db.execute(stmt)
        announcements = result.scalars().all()
        return [
            AnnouncementType(
                id=announcement.id,
                user_id=announcement.user_id,
                class_id=announcement.class_id,
                type=AnnouncementTypeEnum[announcement.type],
                created_at=announcement.created_at,
                updated_at=announcement.updated_at,
            )
            for announcement in announcements
        ]

    @strawberry.field
    async def chats(self, info: strawberry.Info[Context]) -> List[ChatType]:
        db = info.context.db
        stmt = select(ChatModel).where(ChatModel.user_id == self.id)
        result = await db.execute(stmt)
        chats = result.scalars().all()
        return [
            ChatType(
                id=chat.id,
                chat_room_id=chat.chat_room_id,
                user_id=chat.user_id,
                created_at=chat.created_at,
                updated_at=chat.updated_at,
            )
            for chat in chats
        ]

    @strawberry.field
    async def chat_room_members(
        self, info: strawberry.Info[Context]
    ) -> List[ChatRoomMemberType]:
        db = info.context.db
        stmt = select(ChatRoomMemberModel).where(ChatRoomMemberModel.user_id == self.id)
        result = await db.execute(stmt)
        members = result.scalars().all()
        return [
            ChatRoomMemberType(
                id=member.id,
                chat_room_id=member.chat_room_id,
                user_id=member.user_id,
                created_at=member.created_at,
                updated_at=member.updated_at,
            )
            for member in members
        ]
