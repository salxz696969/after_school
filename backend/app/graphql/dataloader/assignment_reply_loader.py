from typing import List, Optional
from sqlalchemy import select
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.user_model import UserModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_assignment_columns, get_assignment_reply_content_columns, get_user_columns


class AssignmentReplyLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentModel]
        ] = DataLoader(load_fn=self._load_assignments)
        self.user_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[UserModel]
        ] = DataLoader(load_fn=self._load_users)
        self.assignment_reply_content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[AssignmentReplyContentModel]
        ] = DataLoader(load_fn=self._load_assignment_reply_contents)

    async def _load_assignments(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentModel]]:
        try:
            fields = keys[0][1]
            assignment_reply_ids = [key[0] for key in keys]
            column_dict = get_assignment_columns(list(fields))
            if "assignment_reply_id" not in fields:
                column_dict["assignment_reply_id"] = AssignmentReplyModel.id
            stmt = select(*column_dict.values()).join(AssignmentReplyModel).where(AssignmentReplyModel.id.in_(assignment_reply_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            replies = result.mappings().all()
            return [AssignmentModel(**reply) for reply in replies]  # type: ignore
        except Exception as e:
            raise e

    async def _load_users(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[UserModel]]:
        try:
            assignment_reply_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_user_columns(list(fields))
            if "assignment_reply_id" not in fields:
                column_dict["assignment_reply_id"] = AssignmentReplyModel.id
            stmt = select(*column_dict.values()).join(AssignmentReplyModel).where(AssignmentReplyModel.id.in_(assignment_reply_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignment_reply_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[AssignmentReplyContentModel]]:
        try:
            fields = keys[0][1]
            assignment_reply_ids = [key[0] for key in keys]
            column_dict = get_assignment_reply_content_columns(list(fields))
            if "assignment_reply_id" not in fields:
                column_dict["assignment_reply_id"] = AssignmentReplyModel.id
            stmt = select(*column_dict.values()).where(AssignmentReplyContentModel.assignment_reply_id.in_(assignment_reply_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [AssignmentReplyContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
