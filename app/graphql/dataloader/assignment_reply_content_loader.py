import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.assignment_reply_content_model import AssignmentReplyContentModel
from app.db.assignment_reply_model import AssignmentReplyModel
from app.db.media_model import MediaModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class AssignmentReplyContentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._assignment_reply_fields: List[str] | None = None
        self._media_fields: List[str] | None = None
        self.assignment_reply_loader: (
            DataLoader[int, Optional[AssignmentReplyModel]] | None
        ) = None
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] | None = None

    def create_assignment_reply_loader(self, fields: List[str]) -> None:
        self._assignment_reply_fields = fields
        self.assignment_reply_loader = DataLoader(load_fn=self._load_assignment_replies)

    def create_media_loader(self, fields: List[str]) -> None:
        self._media_fields = fields
        self.media_loader = DataLoader(load_fn=self._load_medias)

    async def _load_assignment_replies(
        self, keys: List[int]
    ) -> List[Optional[AssignmentReplyModel]]:
        try:
            if not self._assignment_reply_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_reply_content_ids = keys
            column_list = ColumnGetter.get_assignment_reply_columns(
                list(self._assignment_reply_fields)
            )
            stmt = select(*column_list).join(AssignmentReplyContentModel, AssignmentReplyContentModel.assignment_reply_id == AssignmentReplyModel.id).where(AssignmentReplyContentModel.id.in_(assignment_reply_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                replies = result.mappings().all()  # type: ignore
                return [AssignmentReplyModel(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignment replies: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment replies"
            )

    async def _load_medias(self, keys: List[int]) -> List[Optional[List[MediaModel]]]:
        try:
            if not self._media_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_reply_content_ids = keys
            column_list = ColumnGetter.get_media_columns(list(self._media_fields))
            if "assignmentReplyContentId" not in self._media_fields:
                column_list.append(MediaModel.assignment_reply_content_id)
            stmt = select(*column_list).where(MediaModel.assignment_reply_content_id.in_(assignment_reply_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
            return [
                [
                    MediaModel(**media)
                    for media in medias  # type: ignore
                    if media["assignment_reply_content_id"] == content_id
                ]
                for content_id in assignment_reply_content_ids
            ]
        except Exception as e:
            logging.exception(f"Error loading medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to load medias")
