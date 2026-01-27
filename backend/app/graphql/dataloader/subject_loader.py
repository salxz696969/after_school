from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assignment_model import AssignmentModel
from app.models.class_model import ClassModel
from app.models.subject_model import SubjectModel
from strawberry.dataloader import DataLoader


class SubjectLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[int, Optional[ClassModel]] = DataLoader(
            load_fn=lambda ids: self._load_classes(ids, db)
        )
        self.assignment_loader: DataLoader[int, Optional[List[AssignmentModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_assignments(ids, db))
        )

    async def _load_classes(
        self, subject_ids: List[int], db: AsyncSession
    ) -> List[Optional[ClassModel]]:
        stmt = select(ClassModel).join(SubjectModel).where(
            SubjectModel.id.in_(subject_ids)
        )
        result = await db.execute(stmt)
        classes = result.scalars().all()
        class_map = {class_model.id: class_model for class_model in classes}
        return [class_map.get(subject_id) for subject_id in subject_ids]

    async def _load_assignments(
        self, subject_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AssignmentModel]]]:
        stmt = select(AssignmentModel).where(
            AssignmentModel.subject_id.in_(subject_ids)
        )
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        assignment_map: dict[int, List[AssignmentModel]] = {
            subject_id: [] for subject_id in subject_ids
        }
        for assignment in assignments:
            if assignment.subject_id is not None:
                assignment_map[assignment.subject_id].append(assignment)
        return [assignment_map.get(subject_id, []) for subject_id in subject_ids]
