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
from .database import AsyncSessionLocal
from .redis import redis
from typing import AsyncGenerator
from strawberry.fastapi import BaseContext


class Context(BaseContext):
    def __init__(self, redis: Redis, sessionmaker: AsyncSessionLocal):  # type: ignore
        super().__init__()
        self.sessionmaker = sessionmaker # type: ignore
        self.redis = redis  # type: ignore
        self.announcement_content_loader = AnnouncementContentLoader(sessionmaker) # type: ignore
        self.announcement_loader = AnnouncementLoader(sessionmaker) # type: ignore
        self.assignment_content_loader = AssignmentContentLoader(sessionmaker) # type: ignore
        self.assignment_loader = AssignmentLoader(sessionmaker) # type: ignore
        self.assignment_reply_content_loader = AssignmentReplyContentLoader(
            sessionmaker # type: ignore
        )
        self.assignment_reply_loader = AssignmentReplyLoader(sessionmaker) # type: ignore
        self.chat_content_loader = ChatContentLoader(sessionmaker) # type: ignore
        self.chat_loader = ChatLoader(sessionmaker) # type: ignore
        self.chat_room_loader = ChatRoomLoader(sessionmaker) # type: ignore
        self.chat_room_member_loader = ChatRoomMemberLoader(sessionmaker) # type: ignore
        self.class_loader = ClassLoader(sessionmaker) # type: ignore
        self.media_loader = MediaLoader(sessionmaker) # type: ignore
        self.schedule_content_loader = ScheduleContentLoader(sessionmaker) # type: ignore
        self.schedule_loader = ScheduleLoader(sessionmaker) # type: ignore
        self.subject_loader = SubjectLoader(sessionmaker) # type: ignore
        self.user_loader = UserLoader(sessionmaker) # type: ignore


async def get_context() -> AsyncGenerator[Context, None]:
    yield Context(redis=redis, sessionmaker=AsyncSessionLocal)  # type: ignore
