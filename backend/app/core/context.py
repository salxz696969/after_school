from redis.asyncio import Redis

from app.graphql.dataloader.announcement_content_loader import AnnouncementContentLoader
from app.graphql.dataloader.announcement_loader import AnnouncementLoader
from app.graphql.dataloader.assignment_content_loader import AssignmentContentLoader
from app.graphql.dataloader.assignment_loader import AssignmentLoader
from app.graphql.dataloader.assignment_reply_content_loader import (
    AssignmentReplyContentLoader,
)
from app.graphql.dataloader.assignment_reply_loader import AssignmentReplyLoader
from app.graphql.dataloader.chat_content_loader import ChatContentLoader
from app.graphql.dataloader.chat_loader import ChatLoader
from app.graphql.dataloader.chat_room_loader import ChatRoomLoader
from app.graphql.dataloader.chat_room_member_loader import ChatRoomMemberLoader
from app.graphql.dataloader.class_loader import ClassLoader
from app.graphql.dataloader.media_loader import MediaLoader
from app.graphql.dataloader.schedule_content_loader import ScheduleContentLoader
from app.graphql.dataloader.schedule_loader import ScheduleLoader
from app.graphql.dataloader.subject_loader import SubjectLoader
from app.graphql.dataloader.user_loader import UserLoader


from .database import get_db
from .redis import redis
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    def __init__(self, db: AsyncSession, redis: Redis):  # type: ignore
        super().__init__()
        self.db = db
        self.redis = redis  # type: ignore
        self.announcement_content_loader = AnnouncementContentLoader(db)
        self.announcement_loader = AnnouncementLoader(db)
        self.assignment_content_loader = AssignmentContentLoader(db)
        self.assignment_loader = AssignmentLoader(db)
        self.assignment_reply_content_loader = AssignmentReplyContentLoader(db)
        self.assignment_reply_loader = AssignmentReplyLoader(db)
        self.chat_content_loader = ChatContentLoader(db)
        self.chat_loader = ChatLoader(db)
        self.chat_room_loader = ChatRoomLoader(db)
        self.chat_room_member_loader = ChatRoomMemberLoader(db)
        self.class_loader = ClassLoader(db)
        self.media_loader = MediaLoader(db)
        self.schedule_content_loader = ScheduleContentLoader(db)
        self.schedule_loader = ScheduleLoader(db)
        self.subject_loader = SubjectLoader(db)
        self.user_loader = UserLoader(db)


async def get_context() -> AsyncGenerator[Context, None]:
    async for db in get_db():
        yield Context(db=db, redis=redis)
