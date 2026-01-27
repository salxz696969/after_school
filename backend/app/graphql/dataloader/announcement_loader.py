from typing import List, Optional

from sqlalchemy import select
from strawberry.dataloader import DataLoader
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.class_model import ClassModel
from app.models.user_model import UserModel


class AnnouncementLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[int, Optional[UserModel]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )
        self.class_loader: DataLoader[int, Optional[ClassModel]] = DataLoader(
            load_fn=lambda ids: self._load_classes(ids, db)
        )
        self.announcement_content_loader: DataLoader[
            int, Optional[AnnouncementContentModel]
        ] = DataLoader(load_fn=lambda ids: self._load_announcement_contents(ids, db))

    async def _load_users(
        self, announcement_ids: List[int], db: AsyncSession
    ) -> List[Optional[UserModel]]:
        stmt = (
            select(UserModel)
            .join(AnnouncementModel)
            .where(AnnouncementModel.id.in_(announcement_ids))
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map = {user.id: user for user in users}
        return [user_map.get(announcement_id) for announcement_id in announcement_ids]

    async def _load_classes(
        self, announcement_ids: List[int], db: AsyncSession
    ) -> List[Optional[ClassModel]]:

        stmt = (
            select(ClassModel)
            .join(AnnouncementModel)
            .where(AnnouncementModel.id.in_(announcement_ids))
        )
        result = await db.execute(stmt)
        classes = result.scalars().all()
        class_map = {class_.id: class_ for class_ in classes}
        return [class_map.get(announcement_id) for announcement_id in announcement_ids]

    async def _load_announcement_contents(
        self, announcement_ids: List[int], db: AsyncSession
    ) -> List[Optional[AnnouncementContentModel]]:
        stmt = select(AnnouncementContentModel).where(
            AnnouncementContentModel.announcement_id.in_(announcement_ids)
        )
        result = await db.execute(stmt)
        contents = result.scalars().all()
        content_map = {content.id: content for content in contents}
        return [
            content_map.get(announcement_id) for announcement_id in announcement_ids
        ]
