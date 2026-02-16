import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.db.announcement_content_model import AnnouncementContentModel
from app.db.announcement_model import AnnouncementModel
from app.db.class_model import ClassModel
from app.db.user_model import UserModel
from app.utils.get_column import ColumnGetter


class AnnouncementLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._user_fields: List[str] | None = None
        self._class_fields: List[str] | None = None
        self._content_fields: List[str] | None = None
        self.user_loader: DataLoader[int, Optional[UserModel]] | None = None
        self.class_loader: DataLoader[int, Optional[ClassModel]] | None = None
        self.announcement_content_loader: (
            DataLoader[int, Optional[AnnouncementContentModel]] | None
        ) = None

    def create_user_loader(self, fields: List[str]) -> None:
        self._user_fields = fields
        self.user_loader = DataLoader(load_fn=self._load_users)

    def create_class_loader(self, fields: List[str]) -> None:
        self._class_fields = fields
        self.class_loader = DataLoader(load_fn=self._load_classes)

    def create_announcement_content_loader(self, fields: List[str]) -> None:
        self._content_fields = fields
        self.announcement_content_loader = DataLoader(
            load_fn=self._load_announcement_contents
        )

    async def _load_users(self, keys: List[int]) -> List[Optional[UserModel]]:
        try:
            if not self._user_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            announcement_ids = keys
            column_list = ColumnGetter.get_user_columns(list(self._user_fields))
            stmt = select(*column_list).join(AnnouncementModel, UserModel.id == AnnouncementModel.user_id).where(AnnouncementModel.id.in_(announcement_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            raise HTTPException(status_code=500, detail="Failed to load users")

    async def _load_classes(self, keys: List[int]) -> List[Optional[ClassModel]]:
        try:
            if not self._class_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            announcement_ids = keys
            column_list = ColumnGetter.get_class_columns(list(self._class_fields))
            stmt = select(*column_list).join(AnnouncementModel, AnnouncementModel.class_id == ClassModel.id).where(AnnouncementModel.id.in_(announcement_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                classes = result.mappings().all()  # type: ignore
                return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading classes: {e}")
            raise HTTPException(status_code=500, detail="Failed to load classes")

    async def _load_announcement_contents(
        self, keys: List[int]
    ) -> List[Optional[AnnouncementContentModel]]:
        try:
            if not self._content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            announcement_ids = keys
            column_list = ColumnGetter.get_announcement_content_columns(
                list(self._content_fields)
            )
            if "announcementId" not in self._content_fields:
                column_list.append(AnnouncementContentModel.announcement_id)
            stmt = select(*column_list).where(AnnouncementContentModel.announcement_id.in_(announcement_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AnnouncementContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading announcement contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load announcement contents"
            )
