from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.media_model import MediaModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_media_columns, get_schedule_columns


class ScheduleContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.schedule_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ScheduleModel]
        ] = DataLoader(load_fn=self._load_schedule)
        self.media_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[MediaModel]]
        ] = DataLoader(load_fn=self._load_medias)

    async def _load_schedule(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ScheduleModel]]:
        try:
            fields = keys[0][1]
            schedule_content_ids = [key[0] for key in keys]
            column_dict = get_schedule_columns(list(fields))
            stmt = select(*column_dict.values()).join(ScheduleContentModel).where(ScheduleContentModel.id.in_(schedule_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            schedules = result.mappings().all()
            return [ScheduleModel(**schedule) for schedule in schedules]  # type: ignore
        except Exception as e:
            raise e

    async def _load_medias(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[MediaModel]]]:
        try:
            fields = keys[0][1]
            schedule_content_ids = [key[0] for key in keys]
            column_dict = get_media_columns(list(fields))
            if "schedule_content_id" not in fields:
                column_dict["schedule_content_id"] = ScheduleContentModel.id
            stmt = select(*column_dict.values()).where(MediaModel.schedule_content_id.in_(schedule_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            medias = result.mappings().all()
            return [
                [
                    MediaModel(**media)
                    for media in medias
                    if media["schedule_content_id"] == content_id
                ]
                for content_id in schedule_content_ids
            ]
        except Exception as e:
            raise e
