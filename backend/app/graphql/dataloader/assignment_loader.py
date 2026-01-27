from typing import List, Optional
from sqlalchemy import select

from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.subject_model import SubjectModel
from app.models.user_model import UserModel
from app.models.class_model import ClassModel
from app.models.assignment_content_model import AssignmentContentModel
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader


class AssignmentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[int, Optional[UserModel]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )
        self.subject_loader: DataLoader[int, Optional[SubjectModel]] = DataLoader(
            load_fn=lambda ids: self._load_subjects(ids, db)
        )
        self.class_loader: DataLoader[int, Optional[ClassModel]] = DataLoader(
            load_fn=lambda ids: self._load_classes(ids, db)
        )
        self.assignment_reply_loader: DataLoader[
            int, Optional[List[AssignmentReplyModel]]
        ] = DataLoader(load_fn=lambda ids: self._load_assignment_replies(ids, db))
        self.assignment_content_loader: DataLoader[
            int, Optional[AssignmentContentModel]
        ] = DataLoader(load_fn=lambda ids: self._load_assignment_contents(ids, db))

    async def _load_users(
        self, assignment_ids: List[int], db: AsyncSession
    ) -> List[Optional[UserModel]]:
        stmt = (
            select(UserModel)
            .join(AssignmentModel)
            .where(AssignmentModel.id.in_(assignment_ids))
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map = {user.id: user for user in users}
        return [user_map.get(assignment_id) for assignment_id in assignment_ids]

    async def _load_subjects(
        self, assignment_ids: List[int], db: AsyncSession
    ) -> List[Optional[SubjectModel]]:
        stmt = (
            select(SubjectModel)
            .join(AssignmentModel)
            .where(AssignmentModel.id.in_(assignment_ids))
        )
        result = await db.execute(stmt)
        subjects = result.scalars().all()
        subject_map = {subject.id: subject for subject in subjects}
        return [subject_map.get(assignment_id) for assignment_id in assignment_ids]

    async def _load_classes(
        self, assignment_ids: List[int], db: AsyncSession
    ) -> List[Optional[ClassModel]]:
        stmt = (
            select(ClassModel)
            .join(AssignmentModel)
            .where(AssignmentModel.id.in_(assignment_ids))
        )
        result = await db.execute(stmt)
        classes = result.scalars().all()
        class_map = {class_.id: class_ for class_ in classes}
        return [class_map.get(assignment_id) for assignment_id in assignment_ids]

    async def _load_assignment_replies(
        self, assignment_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        stmt = select(AssignmentReplyModel).where(
            AssignmentReplyModel.assignment_id.in_(assignment_ids)
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        reply_map: dict[int, list[AssignmentReplyModel]] = {
            assignment_id: [] for assignment_id in assignment_ids
        }
        for reply in replies:
            if reply.assignment_id is not None:
                reply_map[reply.assignment_id].append(reply)
        return [reply_map.get(assignment_id, []) for assignment_id in assignment_ids]

    async def _load_assignment_contents(
        self, assignment_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentContentModel]]:

        stmt = select(AssignmentContentModel).where(
            AssignmentContentModel.assignment_id.in_(assignment_ids)
        )
        result = await db.execute(stmt)
        contents = result.scalars().all()
        content_map = {content.assignment_id: content for content in contents}
        return [content_map.get(assignment_id) for assignment_id in assignment_ids]
