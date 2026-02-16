import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.assignment_model import AssignmentModel
from app.db.assignment_reply_model import AssignmentReplyModel
from app.db.user_model import UserModel
from app.db.assignment_reply_content_model import AssignmentReplyContentModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class AssignmentReplyLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._assignment_fields: List[str] | None = None
        self._user_fields: List[str] | None = None
        self._content_fields: List[str] | None = None
        self.assignment_loader: DataLoader[int, Optional[AssignmentModel]] | None = None
        self.user_loader: DataLoader[int, Optional[UserModel]] | None = None
        self.assignment_reply_content_loader: (
            DataLoader[int, Optional[AssignmentReplyContentModel]] | None
        ) = None

    def create_assignment_loader(self, fields: List[str]) -> None:
        self._assignment_fields = fields
        self.assignment_loader = DataLoader(load_fn=self._load_assignments)

    def create_user_loader(self, fields: List[str]) -> None:
        self._user_fields = fields
        self.user_loader = DataLoader(load_fn=self._load_users)

    def create_assignment_reply_content_loader(self, fields: List[str]) -> None:
        self._content_fields = fields
        self.assignment_reply_content_loader = DataLoader(
            load_fn=self._load_assignment_reply_contents
        )

    async def _load_assignments(
        self, keys: List[int]
    ) -> List[Optional[AssignmentModel]]:
        try:
            if not self._assignment_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_reply_ids = keys
            column_list = ColumnGetter.get_assignment_columns(
                list(self._assignment_fields)
            )
            stmt = select(*column_list).join(AssignmentReplyModel, AssignmentReplyModel.assignment_id == AssignmentModel.id).where(AssignmentReplyModel.id.in_(assignment_reply_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                replies = result.mappings().all()  # type: ignore
                return [AssignmentModel(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to load assignments")

    async def _load_users(self, keys: List[int]) -> List[Optional[UserModel]]:
        try:
            if not self._user_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_reply_ids = keys
            column_list = ColumnGetter.get_user_columns(list(self._user_fields))
            stmt = select(*column_list).join(AssignmentReplyModel, AssignmentReplyModel.user_id == UserModel.id).where(AssignmentReplyModel.id.in_(assignment_reply_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            raise HTTPException(status_code=500, detail="Failed to load users")

    async def _load_assignment_reply_contents(
        self, keys: List[int]
    ) -> List[Optional[AssignmentReplyContentModel]]:
        try:
            if not self._content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            assignment_reply_ids = keys
            column_list = ColumnGetter.get_assignment_reply_content_columns(
                list(self._content_fields)
            )
            if "assignmentReplyId" not in self._content_fields:
                column_list.append(AssignmentReplyContentModel.assignment_reply_id)
            stmt = select(*column_list).where(AssignmentReplyContentModel.assignment_reply_id.in_(assignment_reply_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [AssignmentReplyContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading assignment reply contents: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment reply contents"
            )
