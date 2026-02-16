import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.media_model import MediaModel
from app.db.schedule_content_model import ScheduleContentModel
from app.db.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class ScheduleContentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._schedule_fields: List[str] | None = None
        self._media_fields: List[str] | None = None
        self.schedule_loader: DataLoader[int, Optional[ScheduleModel]] | None = None
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] | None = None

    def create_schedule_loader(self, fields: List[str]) -> None:
        self._schedule_fields = fields
        self.schedule_loader = DataLoader(load_fn=self._load_schedule)

    def create_media_loader(self, fields: List[str]) -> None:
        self._media_fields = fields
        self.media_loader = DataLoader(load_fn=self._load_medias)

    async def _load_schedule(self, keys: List[int]) -> List[Optional[ScheduleModel]]:
        try:
            if not self._schedule_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            schedule_content_ids = keys
            column_list = ColumnGetter.get_schedule_columns(list(self._schedule_fields))
            stmt = select(*column_list).join(ScheduleContentModel, ScheduleContentModel.schedule_id == ScheduleModel.id).where(ScheduleContentModel.id.in_(schedule_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                schedules = result.mappings().all()  # type: ignore
                return [ScheduleModel(**schedule) for schedule in schedules]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading schedules: {e}")
            raise HTTPException(status_code=500, detail="Failed to load schedules")

    async def _load_medias(self, keys: List[int]) -> List[Optional[List[MediaModel]]]:
        try:
            if not self._media_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            schedule_content_ids = keys
            column_list = ColumnGetter.get_media_columns(list(self._media_fields))
            if "scheduleContentId" not in self._media_fields:
                column_list.append(MediaModel.schedule_content_id)
            stmt = select(*column_list).where(MediaModel.schedule_content_id.in_(schedule_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
                return [
                    [
                        MediaModel(**media)
                        for media in medias  # type: ignore
                        if media["schedule_content_id"] == content_id
                    ]
                    for content_id in schedule_content_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to load medias")
