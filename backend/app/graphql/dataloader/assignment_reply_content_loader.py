from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.media_model import MediaModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_assignment_columns, get_media_columns


class AssignmentReplyContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_reply_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentReplyModel]
        ] = DataLoader(load_fn=self._load_assignments)
        self.media_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[MediaModel]]
        ] = DataLoader(load_fn=self._load_medias)

    async def _load_assignments(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentReplyModel]]:
        try:
            assignment_reply_content_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_columns(list(fields))
            stmt = select(*column_dict.values()).join(AssignmentReplyContentModel).where(AssignmentReplyContentModel.id.in_(assignment_reply_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            replies = result.mappings().all()
            return [AssignmentReplyModel(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            raise e

    async def _load_medias(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[MediaModel]]]:
        try:
            assignment_reply_content_ids = [key[0] for key in keys]
            fields = keys[0][1]
            columns = get_media_columns(list(fields))
            if "assignment_reply_content_id" not in fields:
                columns["assignment_reply_content_id"] = (
                    MediaModel.assignment_reply_content_id
                )
            stmt = select(*columns.values()).where(MediaModel.assignment_reply_content_id.in_(assignment_reply_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            medias = result.mappings().all()
            return [
                [
                    MediaModel(**media)
                    for media in medias
                    if media["assignment_reply_content_id"] == content_id
                ]
                for content_id in assignment_reply_content_ids
            ]
        except Exception as e:
            raise e
