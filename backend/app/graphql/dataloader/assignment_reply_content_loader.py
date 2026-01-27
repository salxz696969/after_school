from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.media_model import MediaModel
from strawberry.dataloader import DataLoader


class AssignmentReplyContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_reply_loader: DataLoader[
            int, Optional[AssignmentReplyModel]
        ] = DataLoader(load_fn=lambda ids: self._load_assignments(ids, db))
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] = DataLoader(
            load_fn=lambda ids: self._load_medias(ids, db)
        )

    async def _load_assignments(
        self, assignment_reply_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentReplyModel]]:
        stmt = (
            select(AssignmentModel)
            .join(AssignmentReplyContentModel)
            .where(AssignmentReplyContentModel.id.in_(assignment_reply_content_ids))
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        reply_map = {reply.id: reply for reply in replies}
        return [
            reply_map.get(content_reply_id)
            for content_reply_id in assignment_reply_content_ids
        ]

    async def _load_medias(
        self, assignment_reply_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[MediaModel]]]:

        stmt = select(MediaModel).where(
            MediaModel.assignment_reply_content_id.in_(assignment_reply_content_ids)
        )
        result = await db.execute(stmt)
        medias = result.scalars().all()
        media_map: dict[int, list[MediaModel]] = {
            assignment_reply_content_id: []
            for assignment_reply_content_id in assignment_reply_content_ids
        }
        for media in medias:
            if media.assignment_reply_content_id is not None:
                media_map[media.assignment_reply_content_id].append(media)
        return [
            media_map.get(content_reply_id, [])
            for content_reply_id in assignment_reply_content_ids
        ]
