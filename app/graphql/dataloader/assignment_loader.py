import logging
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy import select

from app.db.assignment_model import AssignmentModel
from app.db.assignment_reply_model import AssignmentReplyModel
from app.db.subject_model import SubjectModel
from app.db.user_model import UserModel
from app.db.class_model import ClassModel
from app.db.assignment_content_model import AssignmentContentModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class AssignmentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._user_fields: List[str] | None = None
        self._subject_fields: List[str] | None = None
        self._class_fields: List[str] | None = None
        self._reply_fields: List[str] | None = None
        self._content_fields: List[str] | None = None
        self.user_loader: DataLoader[int, Optional[UserModel]] | None = None
        self.subject_loader: DataLoader[int, Optional[SubjectModel]] | None = None
        self.class_loader: DataLoader[int, Optional[ClassModel]] | None = None
        self.assignment_reply_loader: (
            DataLoader[int, Optional[List[AssignmentReplyModel]]] | None
        ) = None
        self.assignment_content_loader: (
            DataLoader[int, Optional[AssignmentContentModel]] | None
        ) = None

    def create_user_loader(self, fields: List[str]) -> None:
        self._user_fields = fields
        self.user_loader = DataLoader(load_fn=self._load_users)

    def create_subject_loader(self, fields: List[str]) -> None:
        self._subject_fields = fields
        self.subject_loader = DataLoader(load_fn=self._load_subjects)

    def create_class_loader(self, fields: List[str]) -> None:
        self._class_fields = fields
        self.class_loader = DataLoader(load_fn=self._load_classes)

    def create_assignment_reply_loader(self, fields: List[str]) -> None:
        self._reply_fields = fields
        self.assignment_reply_loader = DataLoader(load_fn=self._load_assignment_replies)

    def create_assignment_content_loader(self, fields: List[str]) -> None:
        self._content_fields = fields
        self.assignment_content_loader = DataLoader(
            load_fn=self._load_assignment_contents
        )

    async def _load_users(self, keys: List[int]) -> List[Optional[UserModel]]:
        try:
            if not self._user_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_ids = keys
            column_list = ColumnGetter.get_user_columns(list(self._user_fields))
            stmt = select(*column_list).join(AssignmentModel, AssignmentModel.user_id == UserModel.id).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            raise HTTPException(status_code=500, detail="Failed to load users")

    async def _load_subjects(self, keys: List[int]) -> List[Optional[SubjectModel]]:
        try:
            if not self._subject_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_ids = keys
            column_list = ColumnGetter.get_subject_columns(list(self._subject_fields))
            stmt = select(*column_list).join(AssignmentModel, AssignmentModel.subject_id == SubjectModel.id).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                subjects = result.mappings().all()  # type: ignore
                return [SubjectModel(**subject) for subject in subjects]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading subjects: {e}")
            raise HTTPException(status_code=500, detail="Failed to load subjects")

    async def _load_classes(self, keys: List[int]) -> List[Optional[ClassModel]]:
        try:
            if not self._class_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_ids = keys
            column_list = ColumnGetter.get_class_columns(list(self._class_fields))
            stmt = select(*column_list).join(AssignmentModel, AssignmentModel.class_id == ClassModel.id).where(AssignmentModel.id.in_(assignment_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                classes = result.mappings().all()  # type: ignore
                return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading classes: {e}")
            raise HTTPException(status_code=500, detail="Failed to load classes")

    async def _load_assignment_replies(
        self, keys: List[int]
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        try:
            if not self._reply_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_ids = keys
            column_list = ColumnGetter.get_assignment_reply_columns(
                list(self._reply_fields)
            )
            if "assignmentId" not in self._reply_fields:
                column_list.append(AssignmentReplyModel.assignment_id)
            stmt = select(*column_list).where(AssignmentReplyModel.assignment_id.in_(assignment_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                replies = result.mappings().all()  # type: ignore
                return [
                    [
                        AssignmentReplyModel(**reply)
                        for reply in replies  # type: ignore
                        if reply["assignment_id"] == assignment_id
                    ]
                    for assignment_id in assignment_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading assignment replies: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment replies"
            )

    async def _load_assignment_contents(
        self, keys: List[int]
    ) -> List[Optional[AssignmentContentModel]]:
        try:
            if not self._content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_ids = keys
            column_list = ColumnGetter.get_assignment_content_columns(
                list(self._content_fields)
            )
            if "assignmentId" not in self._content_fields:
                column_list.append(AssignmentContentModel.assignment_id)
            stmt = select(*column_list).where(AssignmentContentModel.assignment_id.in_(assignment_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AssignmentContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignment contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment contents"
            )
