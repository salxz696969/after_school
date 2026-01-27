from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.media_model import MediaModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader


class ScheduleContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.schedule_loader: DataLoader[int, Optional[ScheduleModel]] = DataLoader(
            load_fn=lambda ids: self._load_schedule(ids, db)
        )
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] = DataLoader(
            load_fn=lambda ids: self._load_medias(ids, db)
        )

    async def _load_schedule(
        self, schedule_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[ScheduleModel]]:
        stmt = (
            select(ScheduleModel)
            .join(ScheduleContentModel)
            .where(ScheduleContentModel.id.in_(schedule_content_ids))
        )
        result = await db.execute(stmt)
        schedules = result.scalars().all()
        schedule_map = {schedule.id: schedule for schedule in schedules}
        return [schedule_map.get(content_id) for content_id in schedule_content_ids]

    async def _load_medias(
        self, schedule_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[MediaModel]]]:
        stmt = select(MediaModel).where(
            MediaModel.schedule_content_id.in_(schedule_content_ids)
        )
        result = await db.execute(stmt)
        medias = result.scalars().all()
        media_map: dict[int, List[MediaModel]] = {
            content_id: [] for content_id in schedule_content_ids
        }
        for media in medias:
            if media.schedule_content_id is not None:
                media_map[media.schedule_content_id].append(media)
        return [media_map.get(content_id, []) for content_id in schedule_content_ids]
