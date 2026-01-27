from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.class_model import ClassModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader


class ScheduleLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[int, Optional[ClassModel]] = DataLoader(
            load_fn=lambda ids: self._load_classes(ids, db)
        )
        self.content_loader: DataLoader[int, Optional[ScheduleContentModel]] = (
            DataLoader(load_fn=lambda ids: self._load_contents(ids, db))
        )

    async def _load_classes(
        self, schedule_ids: List[int], db: AsyncSession
    ) -> List[Optional[ClassModel]]:
        stmt = (
            select(ClassModel)
            .join(ScheduleModel)
            .where(ScheduleModel.id.in_(schedule_ids))
        )
        result = await db.execute(stmt)
        classes = result.scalars().all()
        class_map = {class_model.id: class_model for class_model in classes}
        return [class_map.get(schedule_id) for schedule_id in schedule_ids]

    async def _load_contents(
        self, schedule_ids: List[int], db: AsyncSession
    ) -> List[Optional[ScheduleContentModel]]:
        stmt = select(ScheduleContentModel).where(
            ScheduleContentModel.schedule_id.in_(schedule_ids)
        )
        result = await db.execute(stmt)
        contents = result.scalars().all()
        content_map = {content.schedule_id: content for content in contents}
        return [content_map.get(schedule_id) for schedule_id in schedule_ids]
