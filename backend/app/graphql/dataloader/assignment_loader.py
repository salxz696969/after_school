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

from app.utils.get_column import (
    get_assignment_content_columns,
    get_assignment_reply_columns,
    get_class_columns,
    get_subject_columns,
    get_user_columns,
)


class AssignmentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[UserModel]
        ] = DataLoader(load_fn=self._load_users)
        self.subject_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[SubjectModel]
        ] = DataLoader(load_fn=self._load_subjects)
        self.class_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ClassModel]
        ] = DataLoader(load_fn=self._load_classes)
        self.assignment_reply_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AssignmentReplyModel]]
        ] = DataLoader(load_fn=self._load_assignment_replies)
        self.assignment_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentContentModel]
        ] = DataLoader(load_fn=self._load_assignment_contents)

    async def _load_users(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[UserModel]]:
        try:
            fields = keys[0][1]
            assignment_ids = [key[0] for key in keys]
            column_dict = get_user_columns(list(fields))
            stmt = select(*column_dict.values()).join(AssignmentModel).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            raise e

    async def _load_subjects(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[SubjectModel]]:
        try:
            fields = keys[0][1]
            assignment_ids = [key[0] for key in keys]
            column_dict = get_subject_columns(list(fields))
            stmt = select(*column_dict.values()).join(AssignmentModel).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            subjects = result.mappings().all()
            return [SubjectModel(**subject) for subject in subjects]  # type: ignore
        except Exception as e:
            raise e

    async def _load_classes(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ClassModel]]:
        try:
            fields = keys[0][1]
            assignment_ids = [key[0] for key in keys]
            column_dict = get_class_columns(list(fields))
            stmt = select(*column_dict.values()).join(AssignmentModel).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            classes = result.mappings().all()
            return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignment_replies(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        try:
            fields = keys[0][1]
            assignment_ids = [key[0] for key in keys]
            column_dict = get_assignment_reply_columns(list(fields))
            if "assignment_id" not in fields:
                column_dict["assignment_id"] = AssignmentReplyModel.assignment_id
            stmt = select(*column_dict.values()).where(AssignmentReplyModel.assignment_id.in_(assignment_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            replies = result.mappings().all()
            return [
                [
                    AssignmentReplyModel(**reply)
                    for reply in replies
                    if reply["assignment_id"] == assignment_id
                ]
                for assignment_id in assignment_ids
            ]
        except Exception as e:
            raise e

    async def _load_assignment_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentContentModel]]:
        try:
            assignment_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_content_columns(list(fields))
            if "assignment_id" not in fields:
                column_dict["assignment_id"] = AssignmentContentModel.assignment_id
            stmt = select(*column_dict.values()).where(AssignmentContentModel.assignment_id.in_(assignment_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AssignmentContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
