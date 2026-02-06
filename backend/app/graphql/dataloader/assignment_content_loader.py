from typing import List, Optional
from sqlalchemy import select
from app.models.assignment_content_model import AssignmentContentModel
from app.models.assignment_model import AssignmentModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_assignment_columns, get_media_columns


class AssignmentContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentModel]
        ] = DataLoader(load_fn=self._load_assignments)
        self.media_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[MediaModel]]
        ] = DataLoader(load_fn=self._load_medias)

    async def _load_assignments(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentModel]]:
        try:
            fields = keys[0][1]
            assignment_content_ids = [key[0] for key in keys]
            column_dict = get_assignment_columns(list(fields))
            stmt = select(*column_dict.values()).join(AssignmentContentModel).where(AssignmentContentModel.id.in_(assignment_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignments = result.mappings().all()
            return [AssignmentModel(**assignment) for assignment in assignments]  # type: ignore
        except Exception as e:
            raise e

    async def _load_medias(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[MediaModel]]]:
        try:
            fields = keys[0][1]
            assignment_content_ids = [key[0] for key in keys]
            column_dict = get_media_columns(list(fields))
            if "assignment_content_id" not in fields:
                column_dict["assignment_content_id"] = MediaModel.assignment_content_id
            stmt = select(*column_dict.values()).where(MediaModel.assignment_content_id.in_(assignment_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            medias = result.mappings().all()
            return [
                [
                    MediaModel(**media)
                    for media in medias
                    if media["assignment_content_id"] == content_id
                ]
                for content_id in assignment_content_ids
            ]
        except Exception as e:
            raise e
