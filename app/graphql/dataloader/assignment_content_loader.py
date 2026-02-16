import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.db.assignment_content_model import AssignmentContentModel
from app.db.assignment_model import AssignmentModel
from app.db.media_model import MediaModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import ColumnGetter


class AssignmentContentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._assignment_fields: List[str] | None = None
        self._media_fields: List[str] | None = None
        self.assignment_loader: DataLoader[int, Optional[AssignmentModel]] | None = None
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] | None = None

    def create_assignment_loader(self, fields: List[str]) -> None:
        self._assignment_fields = fields
        self.assignment_loader = DataLoader(load_fn=self._load_assignments)

    def create_media_loader(self, fields: List[str]) -> None:
        self._media_fields = fields
        self.media_loader = DataLoader(load_fn=self._load_medias)

    async def _load_assignments(
        self, keys: List[int]
    ) -> List[Optional[AssignmentModel]]:
        try:
            if not self._assignment_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_content_ids = keys
            column_list = ColumnGetter.get_assignment_columns(
                list(self._assignment_fields)
            )
            stmt = select(*column_list).join(AssignmentContentModel, AssignmentContentModel.assignment_id == AssignmentModel.id).where(AssignmentContentModel.id.in_(assignment_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignments = result.mappings().all()  # type: ignore
                return [AssignmentModel(**assignment) for assignment in assignments]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to load assignments")

    async def _load_medias(self, keys: List[int]) -> List[Optional[List[MediaModel]]]:
        try:
            if not self._media_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_content_ids = keys
            column_list = ColumnGetter.get_media_columns(list(self._media_fields))
            if "assignmentContentId" not in self._media_fields:
                column_list.append(MediaModel.assignment_content_id)
            stmt = select(*column_list).where(MediaModel.assignment_content_id.in_(assignment_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
                return [
                    [
                        MediaModel(**media)
                        for media in medias  # type: ignore
                        if media["assignment_content_id"] == content_id
                    ]
                    for content_id in assignment_content_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to load medias")
