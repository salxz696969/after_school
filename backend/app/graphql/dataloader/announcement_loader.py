from typing import List, Optional
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.class_model import ClassModel
from app.models.user_model import UserModel
from app.utils.get_column import (
    get_announcement_content_columns,
    get_class_columns,
    get_user_columns,
)


class AnnouncementLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[UserModel]
        ] = DataLoader(load_fn=self._load_users)
        self.class_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ClassModel]
        ] = DataLoader(load_fn=self._load_classes)
        self.announcement_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AnnouncementContentModel]
        ] = DataLoader(load_fn=self._load_announcement_contents)

    async def _load_users(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[UserModel]]:
        try:
            fields = keys[0][1]
            announcement_ids = [key[0] for key in keys]
            column_dict = get_user_columns(list(fields))
            stmt = select(*column_dict.values()).join(AnnouncementModel, UserModel.id == AnnouncementModel.user_id).where(AnnouncementModel.id.in_(announcement_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            raise e

    async def _load_classes(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ClassModel]]:
        try:
            announcement_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_class_columns(list(fields))
            stmt = select(*column_dict.values()).join(AnnouncementModel).where(AnnouncementModel.id.in_(announcement_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            classes = result.mappings().all()
            return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            raise e

    async def _load_announcement_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AnnouncementContentModel]]:
        try:
            fields = keys[0][1]
            announcement_ids = [key[0] for key in keys]
            column_dict = get_announcement_content_columns(list(fields))
            if "announcement_id" not in fields:
                column_dict["announcement_id"] = (
                    AnnouncementContentModel.announcement_id
                )
            stmt = select(*column_dict.values()).where(AnnouncementContentModel.announcement_id.in_(announcement_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AnnouncementContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
