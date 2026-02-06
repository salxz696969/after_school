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

from app.utils.get_column import (
    get_announcement_content_columns,
    get_assignment_content_columns,
    get_assignment_reply_content_columns,
    get_chat_content_columns,
    get_schedule_content_columns,
)


class MediaLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ChatContentModel]
        ] = DataLoader(load_fn=self._load_chat_contents)
        self.schedule_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ScheduleContentModel]
        ] = DataLoader(load_fn=self._load_schedule_contents)
        self.announcement_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AnnouncementContentModel]
        ] = DataLoader(load_fn=self._load_announcement_contents)
        self.assignment_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentContentModel]
        ] = DataLoader(load_fn=self._load_assignment_contents)
        self.assignment_reply_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentReplyContentModel]
        ] = DataLoader(load_fn=self._load_assignment_reply_contents)

    async def _load_chat_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ChatContentModel]]:
        try:
            fields = keys[0][1]
            media_ids = [key[0] for key in keys]
            column_dict = get_chat_content_columns(list(fields))
            stmt = select(*column_dict.values()).join(MediaModel).where(MediaModel.id.in_(media_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            chat_contents = result.mappings().all()
            return [ChatContentModel(**chat_content) for chat_content in chat_contents]  # type: ignore
        except Exception as e:
            raise e

    async def _load_schedule_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ScheduleContentModel]]:
        try:
            media_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_schedule_content_columns(list(fields))

            stmt = select(*column_dict.values()).join(MediaModel).where(MediaModel.id.in_(media_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            schedule_contents = result.mappings().all()
            return [ScheduleContentModel(**schedule_content) for schedule_content in schedule_contents]  # type: ignore
        except Exception as e:
            raise e

    async def _load_announcement_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AnnouncementContentModel]]:
        try:
            media_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_announcement_content_columns(list(fields))
            stmt = select(*column_dict.values()).join(MediaModel).where(MediaModel.id.in_(media_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            announcement_contents = result.mappings().all()
            return [AnnouncementContentModel(**announcement_content) for announcement_content in announcement_contents]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignment_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentContentModel]]:
        try:
            media_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_content_columns(list(fields))
            stmt = select(*column_dict.values()).join(MediaModel).where(MediaModel.id.in_(media_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignment_contents = result.mappings().all()
            return [AssignmentContentModel(**assignment_content) for assignment_content in assignment_contents]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignment_reply_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentReplyContentModel]]:
        try:
            media_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_reply_content_columns(list(fields))
            stmt = select(*column_dict.values()).join(MediaModel).where(MediaModel.id.in_(media_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignment_reply_contents = result.mappings().all()
            return [AssignmentReplyContentModel(**assignment_reply_content) for assignment_reply_content in assignment_reply_contents]  # type: ignore
        except Exception as e:
            raise e
