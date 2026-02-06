from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignment_model import AssignmentModel
from app.models.class_model import ClassModel
from app.models.subject_model import SubjectModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_assignment_columns, get_class_columns


class SubjectLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ClassModel]
        ] = DataLoader(load_fn=self._load_classes)
        self.assignment_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AssignmentModel]]
        ] = DataLoader(load_fn=self._load_assignments)

    async def _load_classes(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ClassModel]]:
        try:
            fields = keys[0][1]
            subject_ids = [key[0] for key in keys]
            column_dict = get_class_columns(list(fields))
            if "subject_id" not in fields:
                column_dict["subject_id"] = SubjectModel.id
            stmt = select(*column_dict.values()).join(SubjectModel).where(SubjectModel.id.in_(subject_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            classes = result.mappings().all()
            return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignments(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            subject_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_columns(list(fields))
            if "subject_id" not in fields:
                column_dict["subject_id"] = SubjectModel.id
            stmt = select(*column_dict.values()).where(AssignmentModel.subject_id.in_(subject_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignments = result.mappings().all()
            return [
                [
                    AssignmentModel(**assignment)
                    for assignment in assignments
                    if assignment["subject_id"] == subject_id
                ]
                for subject_id in subject_ids
            ]
        except Exception as e:
            raise e
