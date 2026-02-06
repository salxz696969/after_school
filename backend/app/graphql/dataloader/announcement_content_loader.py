from typing import List, Optional, Tuple
from strawberry.dataloader import DataLoader
from sqlalchemy import select
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.get_column import get_announcement_columns, get_media_columns


class AnnouncementContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.announcement_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AnnouncementModel]
        ] = DataLoader(load_fn=self._load_announcements)
        self.media_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[MediaModel]]
        ] = DataLoader(load_fn=self._load_medias)

    async def _load_announcements(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AnnouncementModel]]:
        try:
            fields = keys[0][1]
            announcement_content_ids = [key[0] for key in keys]
            column_dict = get_announcement_columns(list(fields))
            stmt = select(*column_dict.values()).join(AnnouncementContentModel).where(AnnouncementContentModel.id.in_(announcement_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            announcements = result.maapings().all()  # type: ignore
            return [AnnouncementModel(**ann) for ann in announcements]  # type: ignore
        except Exception as e:
            raise e

    async def _load_medias(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[MediaModel]]]:
        try:
            fields = keys[0][1]
            announcement_content_ids = [key[0] for key in keys]
            column_dict = get_media_columns(list(fields))
            if "announcement_content_id" not in fields:
                column_dict["announcement_content_id"] = MediaModel.announcement_content_id
            stmt = select(*column_dict.values()).where(MediaModel.announcement_content_id.in_(announcement_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            medias = result.mappings().all()  # type: ignore
            return [
                [
                    MediaModel(**media)
                    for media in medias
                    if media["announcement_content_id"] == content_id
                ]
                for content_id in announcement_content_ids
            ]
        except Exception as e:
            raise e
