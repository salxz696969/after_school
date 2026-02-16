import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.assignment_model import AssignmentModel
from app.db.class_model import ClassModel
from app.db.subject_model import SubjectModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class SubjectLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self.class_loader: DataLoader[int, Optional[ClassModel]] | None = None
        self._assignment_fields: List[str] | None = None
        self.assignment_loader: (
            DataLoader[int, Optional[List[AssignmentModel]]] | None
        ) = None

    def create_class_loader(self, fields: List[str]):
        async def _load_classes(ids: List[int]) -> List[Optional[ClassModel]]:
            try:
                column_list = ColumnGetter.get_class_columns(list(fields))
                stmt = select(*column_list).join(SubjectModel, SubjectModel.class_id == ClassModel.id).where(SubjectModel.id.in_(ids))  # type: ignore
                async with self.sessionmaker() as session:  # type: ignore
                    result = await session.execute(stmt)  # type: ignore
                    classes = result.mappings().all()  # type: ignore
                    return [ClassModel(**cls) for cls in classes]  # type: ignore
            except Exception as e:
                logging.exception(f"Error loading classes: {e}")
                raise HTTPException(status_code=500, detail="Failed to load classes")

        self.class_loader = DataLoader(load_fn=_load_classes)

    def create_assignment_loader(self, fields: List[str]) -> None:
        self._assignment_fields = fields
        self.assignment_loader = DataLoader(load_fn=self._load_assignments)

    async def _load_assignments(
        self, keys: List[int]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            if not self._assignment_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            subject_ids = keys
            column_list = ColumnGetter.get_assignment_columns(
                list(self._assignment_fields)
            )
            if "subjectId" not in self._assignment_fields:
                column_list.append(AssignmentModel.subject_id)
            stmt = select(*column_list).where(AssignmentModel.subject_id.in_(subject_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignments = result.mappings().all()  # type: ignore
                return [
                    [
                        AssignmentModel(**assignment)
                        for assignment in assignments  # type: ignore
                        if assignment["subject_id"] == subject_id
                    ]
                    for subject_id in subject_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to load assignments")
