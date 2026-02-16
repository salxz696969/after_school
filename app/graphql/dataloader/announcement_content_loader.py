import logging
from typing import List, Optional
from fastapi import HTTPException
from strawberry.dataloader import DataLoader
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.db.announcement_content_model import AnnouncementContentModel
from app.db.announcement_model import AnnouncementModel
from app.db.media_model import MediaModel

from app.utils.get_column import ColumnGetter


class AnnouncementContentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._announcement_fields: List[str] | None = None
        self._media_fields: List[str] | None = None
        self.announcement_loader: (
            DataLoader[int, Optional[AnnouncementModel]] | None
        ) = None
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] | None = None

    def create_announcement_loader(self, fields: List[str]) -> None:
        self._announcement_fields = fields
        self.announcement_loader = DataLoader(load_fn=self._load_announcements)

    def create_media_loader(self, fields: List[str]) -> None:
        self._media_fields = fields
        self.media_loader = DataLoader(load_fn=self._load_medias)

    async def _load_announcements(
        self, keys: List[int]
    ) -> List[Optional[AnnouncementModel]]:
        try:
            if not self._announcement_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            announcement_content_ids = keys
            column_list = ColumnGetter.get_announcement_columns(
                list(self._announcement_fields)
            )
            stmt = select(*column_list).join(AnnouncementContentModel, AnnouncementContentModel.announcement_id == AnnouncementModel.id).where(AnnouncementContentModel.id.in_(announcement_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                announcements = result.mappings().all()  # type: ignore
                return [AnnouncementModel(**ann) for ann in announcements]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading announcements: {e}")
            raise HTTPException(status_code=500, detail="Failed to load announcements")

    async def _load_medias(self, keys: List[int]) -> List[Optional[List[MediaModel]]]:
        try:
            if not self._media_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            announcement_content_ids = keys
            column_list = ColumnGetter.get_media_columns(list(self._media_fields))
            if "announcementContentId" not in self._media_fields:
                column_list.append(MediaModel.announcement_content_id)
            stmt = select(*column_list).where(MediaModel.announcement_content_id.in_(announcement_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
                return [
                    [
                        MediaModel(**media)
                        for media in medias  # type: ignore
                        if media["announcement_content_id"] == content_id
                    ]
                    for content_id in announcement_content_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to load medias")
