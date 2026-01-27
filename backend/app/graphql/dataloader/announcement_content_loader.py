from typing import List, Optional
from strawberry.dataloader import DataLoader
from sqlalchemy import select
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession


class AnnouncementContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.announcement_loader: DataLoader[int, Optional[AnnouncementModel]] = (
            DataLoader(load_fn=lambda ids: self._load_announcements(ids, db))
        )
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] = DataLoader(
            load_fn=lambda ids: self._load_medias(ids, db)
        )

    async def _load_announcements(
        self, announcement_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[AnnouncementModel]]:
        stmt = (
            select(AnnouncementModel)
            .join(AnnouncementContentModel)
            .where(AnnouncementContentModel.id.in_(announcement_content_ids))
        )
        result = await db.execute(stmt)
        announcements = result.scalars().all()
        announcement_map = {
            announcement.id: announcement for announcement in announcements
        }
        return [announcement_map.get(cid) for cid in announcement_content_ids]

    async def _load_medias(
        self, announcement_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[MediaModel]]]:
        stmt = select(MediaModel).where(
            MediaModel.announcement_content_id.in_(announcement_content_ids)
        )
        result = await db.execute(stmt)
        medias = result.scalars().all()
        media_map: dict[int, list[MediaModel]] = {
            cid: [] for cid in announcement_content_ids
        }
        for media in medias:
            if media.announcement_content_id is not None:
                media_map[media.announcement_content_id].append(media)
        return [
            media_map.get(content_id, []) for content_id in announcement_content_ids
        ]
