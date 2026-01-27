from typing import List, Optional
from sqlalchemy import select
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.user_model import UserModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader


class AssignmentReplyLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.assignment_loader: DataLoader[int, Optional[AssignmentModel]] = DataLoader(
            load_fn=lambda ids: self._load_assignments(ids, db)
        )
        self.user_loader: DataLoader[int, Optional[UserModel]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )
        self.assignment_reply_content_loader: DataLoader[
            int, Optional[AssignmentReplyContentModel]
        ] = DataLoader(
            load_fn=lambda ids: self._load_assignment_reply_contents(ids, db)
        )

    async def _load_assignments(
        self, assignment_reply_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentModel]]:
        stmt = (
            select(AssignmentModel)
            .join(AssignmentReplyModel)
            .where(AssignmentReplyModel.id.in_(assignment_reply_ids))
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        reply_map = {reply.id: reply for reply in replies}
        return [reply_map.get(reply_id) for reply_id in assignment_reply_ids]

    async def _load_users(
        self, assignment_reply_ids: List[int], db: AsyncSession
    ) -> List[Optional[UserModel]]:
        stmt = (
            select(UserModel)
            .join(AssignmentReplyModel)
            .where(AssignmentReplyModel.id.in_(assignment_reply_ids))
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map = {user.id: user for user in users}
        return [user_map.get(reply_id) for reply_id in assignment_reply_ids]

    async def _load_assignment_reply_contents(
        self, assignment_reply_ids: List[int], db: AsyncSession
    ) -> List[Optional[AssignmentReplyContentModel]]:
        stmt = select(AssignmentReplyContentModel).where(
            AssignmentReplyContentModel.assignment_reply_id.in_(assignment_reply_ids)
        )
        result = await db.execute(stmt)
        contents = result.scalars().all()
        content_map = {content.assignment_reply_id: content for content in contents}
        return [content_map.get(reply_id) for reply_id in assignment_reply_ids]
