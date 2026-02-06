from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.class_model import ClassModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_chat_content_columns, get_class_columns


class ScheduleLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ClassModel]
        ] = DataLoader(load_fn=self._load_classes)
        self.content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ScheduleContentModel]
        ] = DataLoader(load_fn=self._load_contents)

    async def _load_classes(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ClassModel]]:
        try:
            schedule_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_class_columns(list(fields))
            stmt = select(*column_dict.values()).join(ScheduleModel).where(ScheduleModel.id.in_(schedule_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            classes = result.mappings().all()
            return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            raise e

    async def _load_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ScheduleContentModel]]:
        try:
            schedule_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_content_columns(list(fields))
            if "schedule_id" not in fields:
                column_dict["schedule_id"] = ScheduleContentModel.id
            stmt = select(*column_dict.values()).where(ScheduleContentModel.schedule_id.in_(schedule_ids)) # type: ignore
            result = await self.db.execute(stmt) # type: ignore
            contents = result.mappings().all()
            return [ScheduleContentModel(**content) for content in contents] # type: ignore
        except Exception as e:
            raise e
