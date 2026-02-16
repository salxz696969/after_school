import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.class_model import ClassModel
from app.db.schedule_content_model import ScheduleContentModel
from app.db.schedule_model import ScheduleModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class ScheduleLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._class_fields: List[str] | None = None
        self._content_fields: List[str] | None = None
        self.class_loader: DataLoader[int, Optional[ClassModel]] | None = None
        self.content_loader: DataLoader[int, Optional[ScheduleContentModel]] | None = (
            None
        )

    def create_class_loader(self, fields: List[str]) -> None:
        self._class_fields = fields
        self.class_loader = DataLoader(load_fn=self._load_classes)

    def create_content_loader(self, fields: List[str]) -> None:
        self._content_fields = fields
        self.content_loader = DataLoader(load_fn=self._load_contents)

    async def _load_classes(self, keys: List[int]) -> List[Optional[ClassModel]]:
        try:
            if not self._class_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            schedule_ids = keys
            column_list = ColumnGetter.get_class_columns(list(self._class_fields))
            stmt = select(*column_list).join(ScheduleModel, ScheduleModel.class_id == ClassModel.id).where(ScheduleModel.id.in_(schedule_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                classes = result.mappings().all()  # type: ignore
                return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading classes: {e}")
            raise HTTPException(status_code=500, detail="Failed to load classes")

    async def _load_contents(
        self, keys: List[int]
    ) -> List[Optional[ScheduleContentModel]]:
        try:
            if not self._content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            schedule_ids = keys
            column_list = ColumnGetter.get_schedule_content_columns(
                list(self._content_fields)
            )
            if "scheduleId" not in self._content_fields:
                column_list.append(ScheduleContentModel.schedule_id)
            stmt = select(*column_list).where(ScheduleContentModel.schedule_id.in_(schedule_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [ScheduleContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading schedule contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load schedule contents"
            )
