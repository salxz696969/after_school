import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.announcement_content_model import AnnouncementContentModel
from app.db.assignment_content_model import AssignmentContentModel
from app.db.assignment_reply_content_model import AssignmentReplyContentModel
from app.db.chat_content_model import ChatContentModel
from app.db.media_model import MediaModel
from app.db.schedule_content_model import ScheduleContentModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class MediaLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._chat_content_fields: List[str] | None = None
        self._schedule_content_fields: List[str] | None = None
        self._announcement_content_fields: List[str] | None = None
        self._assignment_content_fields: List[str] | None = None
        self._assignment_reply_content_fields: List[str] | None = None
        self.chat_content_loader: DataLoader[int, Optional[ChatContentModel]] | None = (
            None
        )
        self.schedule_content_loader: (
            DataLoader[int, Optional[ScheduleContentModel]] | None
        ) = None
        self.announcement_content_loader: (
            DataLoader[int, Optional[AnnouncementContentModel]] | None
        ) = None
        self.assignment_content_loader: (
            DataLoader[int, Optional[AssignmentContentModel]] | None
        ) = None
        self.assignment_reply_content_loader: (
            DataLoader[int, Optional[AssignmentReplyContentModel]] | None
        ) = None

    def create_chat_content_loader(self, fields: List[str]) -> None:
        self._chat_content_fields = fields
        self.chat_content_loader = DataLoader(load_fn=self._load_chat_contents)

    def create_schedule_content_loader(self, fields: List[str]) -> None:
        self._schedule_content_fields = fields
        self.schedule_content_loader = DataLoader(load_fn=self._load_schedule_contents)

    def create_announcement_content_loader(self, fields: List[str]) -> None:
        self._announcement_content_fields = fields
        self.announcement_content_loader = DataLoader(
            load_fn=self._load_announcement_contents
        )

    def create_assignment_content_loader(self, fields: List[str]) -> None:
        self._assignment_content_fields = fields
        self.assignment_content_loader = DataLoader(
            load_fn=self._load_assignment_contents
        )

    def create_assignment_reply_content_loader(self, fields: List[str]) -> None:
        self._assignment_reply_content_fields = fields
        self.assignment_reply_content_loader = DataLoader(
            load_fn=self._load_assignment_reply_contents
        )

    async def _load_chat_contents(
        self, keys: List[int]
    ) -> List[Optional[ChatContentModel]]:
        try:
            if not self._chat_content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            media_ids = keys
            column_list = ColumnGetter.get_chat_content_columns(
                list(self._chat_content_fields)
            )
            stmt = select(*column_list).join(MediaModel, MediaModel.chat_content_id == ChatContentModel.id).where(MediaModel.id.in_(media_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chat_contents = result.mappings().all()  # type: ignore
                return [ChatContentModel(**chat_content) for chat_content in chat_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading chat contents: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chat contents")

    async def _load_schedule_contents(
        self, keys: List[int]
    ) -> List[Optional[ScheduleContentModel]]:
        try:
            if not self._schedule_content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            media_ids = keys
            column_list = ColumnGetter.get_schedule_content_columns(
                list(self._schedule_content_fields)
            )

            stmt = select(*column_list).join(MediaModel, MediaModel.schedule_content_id == ScheduleContentModel.id).where(MediaModel.id.in_(media_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                schedule_contents = result.mappings().all()  # type: ignore
                return [ScheduleContentModel(**schedule_content) for schedule_content in schedule_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading schedule contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load schedule contents"
            )

    async def _load_announcement_contents(
        self, keys: List[int]
    ) -> List[Optional[AnnouncementContentModel]]:
        try:
            if not self._announcement_content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            media_ids = keys
            column_list = ColumnGetter.get_announcement_content_columns(
                list(self._announcement_content_fields)
            )
            stmt = select(*column_list).join(MediaModel, MediaModel.announcement_content_id == AnnouncementContentModel.id).where(MediaModel.id.in_(media_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                announcement_contents = result.mappings().all()  # type: ignore
                return [AnnouncementContentModel(**announcement_content) for announcement_content in announcement_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading announcement contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load announcement contents"
            )

    async def _load_assignment_contents(
        self, keys: List[int]
    ) -> List[Optional[AssignmentContentModel]]:
        try:
            if not self._assignment_content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            media_ids = keys
            column_list = ColumnGetter.get_assignment_content_columns(
                list(self._assignment_content_fields)
            )
            stmt = select(*column_list).join(MediaModel, MediaModel.assignment_content_id == AssignmentContentModel.id).where(MediaModel.id.in_(media_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignment_contents = result.mappings().all()  # type: ignore
                return [AssignmentContentModel(**assignment_content) for assignment_content in assignment_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignment contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment contents"
            )

    async def _load_assignment_reply_contents(
        self, keys: List[int]
    ) -> List[Optional[AssignmentReplyContentModel]]:
        try:
            if not self._assignment_reply_content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            media_ids = keys
            column_list = ColumnGetter.get_assignment_reply_content_columns(
                list(self._assignment_reply_content_fields)
            )
            stmt = select(*column_list).join(MediaModel, MediaModel.assignment_reply_content_id == AssignmentReplyContentModel.id).where(MediaModel.id.in_(media_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignment_reply_contents = result.mappings().all()  # type: ignore
                return [AssignmentReplyContentModel(**assignment_reply_content) for assignment_reply_content in assignment_reply_contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignment reply contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment reply contents"
            )
