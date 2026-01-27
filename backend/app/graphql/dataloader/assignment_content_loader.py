from typing import List, Optional
from sqlalchemy import select
from app.models.assignment_content_model import AssignmentContentModel
from app.models.assignment_model import AssignmentModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader


class AssignmentContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_loader: DataLoader[int, Optional[AssignmentModel]] = DataLoader(
            load_fn=lambda ids: self._load_assignments(ids, db)
        )
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] = DataLoader(
            load_fn=lambda ids: self._load_medias(ids, db)
        )

    async def _load_assignments(
        self, assignment_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentModel]]:
        stmt = (
            select(AssignmentModel)
            .join(AssignmentContentModel)
            .where(AssignmentContentModel.id.in_(assignment_content_ids))
        )
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        assignment_map = {assignment.id: assignment for assignment in assignments}
        return [assignment_map.get(content_id) for content_id in assignment_content_ids]

    async def _load_medias(
        self, assignment_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[MediaModel]]]:
        stmt = select(MediaModel).where(
            MediaModel.assignment_content_id.in_(assignment_content_ids)
        )
        result = await db.execute(stmt)
        medias = result.scalars().all()
        media_map: dict[int, list[MediaModel]] = {
            content_id: [] for content_id in assignment_content_ids
        }
        for media in medias:
            if media.assignment_content_id is not None:
                media_map[media.assignment_content_id].append(media)
        return [media_map.get(content_id, []) for content_id in assignment_content_ids]
