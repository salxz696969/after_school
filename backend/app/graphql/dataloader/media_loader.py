from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.assignment_content_model import AssignmentContentModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from app.models.chat_content_model import ChatContentModel
from app.models.media_model import MediaModel
from app.models.schedule_content_model import ScheduleContentModel
from strawberry.dataloader import DataLoader


class MediaLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_content_loader: DataLoader[int, Optional[ChatContentModel]] = (
            DataLoader(load_fn=lambda ids: self._load_chat_contents(ids, db))
        )
        self.schedule_content_loader: DataLoader[
            int, Optional[ScheduleContentModel]
        ] = DataLoader(load_fn=lambda ids: self._load_schedule_contents(ids, db))
        self.announcement_content_loader: DataLoader[
            int, Optional[AnnouncementContentModel]
        ] = DataLoader(load_fn=lambda ids: self._load_announcement_contents(ids, db))
        self.assignment_content_loader: DataLoader[
            int, Optional[AssignmentContentModel]
        ] = DataLoader(load_fn=lambda ids: self._load_assignment_contents(ids, db))
        self.assignment_reply_content_loader: DataLoader[
            int, Optional[AssignmentReplyContentModel]
        ] = DataLoader(
            load_fn=lambda ids: self._load_assignment_reply_contents(ids, db)
        )

    async def _load_chat_contents(
        self, media_ids: List[int], db: AsyncSession
    ) -> List[Optional[ChatContentModel]]:
        stmt = (
            select(ChatContentModel)
            .join(MediaModel)
            .where(MediaModel.id.in_(media_ids))
        )
        result = await db.execute(stmt)
        chat_contents = result.scalars().all()
        chat_content_map = {
            chat_content.media_id: chat_content for chat_content in chat_contents
        }
        return [chat_content_map.get(media_id) for media_id in media_ids]

    async def _load_schedule_contents(
        self, media_ids: List[int], db: AsyncSession
    ) -> List[Optional[ScheduleContentModel]]:
        stmt = (
            select(ScheduleContentModel)
            .join(MediaModel)
            .where(MediaModel.id.in_(media_ids))
        )
        result = await db.execute(stmt)
        schedule_contents = result.scalars().all()
        schedule_content_map = {
            schedule_content.media_id: schedule_content
            for schedule_content in schedule_contents
        }
        return [schedule_content_map.get(media_id) for media_id in media_ids]

    async def _load_announcement_contents(
        self, media_ids: List[int], db: AsyncSession
    ) -> List[Optional[AnnouncementContentModel]]:
        stmt = (
            select(AnnouncementContentModel)
            .join(MediaModel)
            .where(MediaModel.id.in_(media_ids))
        )
        result = await db.execute(stmt)
        announcement_contents = result.scalars().all()
        announcement_content_map = {
            announcement_content.media_id: announcement_content
            for announcement_content in announcement_contents
        }
        return [announcement_content_map.get(media_id) for media_id in media_ids]

    async def _load_assignment_contents(
        self, media_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentContentModel]]:
        stmt = (
            select(AssignmentContentModel)
            .join(MediaModel)
            .where(MediaModel.id.in_(media_ids))
        )
        result = await db.execute(stmt)
        assignment_contents = result.scalars().all()
        assignment_content_map = {
            assignment_content.media_id: assignment_content
            for assignment_content in assignment_contents
        }
        return [assignment_content_map.get(media_id) for media_id in media_ids]

    async def _load_assignment_reply_contents(
        self, media_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentReplyContentModel]]:
        stmt = (
            select(AssignmentReplyContentModel)
            .join(MediaModel)
            .where(MediaModel.id.in_(media_ids))
        )
        result = await db.execute(stmt)
        assignment_reply_contents = result.scalars().all()
        assignment_reply_content_map = {
            assignment_reply_content.media_id: assignment_reply_content
            for assignment_reply_content in assignment_reply_contents
        }
        return [assignment_reply_content_map.get(media_id) for media_id in media_ids]
