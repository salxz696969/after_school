from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel
from app.models.class_model import ClassModel
from app.models.user_model import UserModel
from strawberry.dataloader import DataLoader


class UserLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[int, Optional[ClassModel]] = DataLoader(
            load_fn=lambda ids: self._load_classes(ids, db)
        )
        self.assignment_loader: DataLoader[int, Optional[List[AssignmentModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_assignments(ids, db))
        )
        self.assignment_reply_loader: DataLoader[
            int, Optional[List[AssignmentReplyModel]]
        ] = DataLoader(load_fn=lambda ids: self._load_assignment_replies(ids, db))
        self.announcement_loader: DataLoader[int, Optional[List[AnnouncementModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_announcements(ids, db))
        )
        self.chat_loader: DataLoader[int, Optional[List[ChatModel]]] = DataLoader(
            load_fn=lambda ids: self._load_chats(ids, db)
        )
        self.chat_room_member_loader: DataLoader[
            int, Optional[List[ChatRoomMemberModel]]
        ] = DataLoader(load_fn=lambda ids: self._load_chat_room_members(ids, db))

    async def _load_classes(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[ClassModel]]:
        stmt = select(ClassModel).join(UserModel).where(UserModel.id.in_(user_ids))
        result = await db.execute(stmt)
        classes = result.scalars().all()
        class_map = {class_model.id: class_model for class_model in classes}
        return [class_map.get(user_id) for user_id in user_ids]

    async def _load_assignments(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AssignmentModel]]]:
        stmt = select(AssignmentModel).where(AssignmentModel.user_id.in_(user_ids))
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        assignment_map: dict[int, List[AssignmentModel]] = {
            user_id: [] for user_id in user_ids
        }
        for assignment in assignments:
            if assignment.user_id is not None:
                assignment_map[assignment.user_id].append(assignment)
        return [assignment_map.get(user_id, []) for user_id in user_ids]

    async def _load_assignment_replies(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        stmt = select(AssignmentReplyModel).where(
            AssignmentReplyModel.user_id.in_(user_ids)
        )
        result = await db.execute(stmt)
        replies = result.scalars().all()
        reply_map: dict[int, List[AssignmentReplyModel]] = {
            user_id: [] for user_id in user_ids
        }
        for reply in replies:
            if reply.user_id is not None:
                reply_map[reply.user_id].append(reply)
        return [reply_map.get(user_id, []) for user_id in user_ids]

    async def _load_announcements(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AnnouncementModel]]]:
        stmt = select(AnnouncementModel).where(AnnouncementModel.user_id.in_(user_ids))
        result = await db.execute(stmt)
        announcements = result.scalars().all()
        announcement_map: dict[int, List[AnnouncementModel]] = {
            user_id: [] for user_id in user_ids
        }
        for announcement in announcements:
            if announcement.user_id is not None:
                announcement_map[announcement.user_id].append(announcement)
        return [announcement_map.get(user_id, []) for user_id in user_ids]

    async def _load_chats(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ChatModel]]]:
        stmt = select(ChatModel).where(ChatModel.user_id.in_(user_ids))
        result = await db.execute(stmt)
        chats = result.scalars().all()
        chat_map: dict[int, List[ChatModel]] = {user_id: [] for user_id in user_ids}
        for chat in chats:
            if chat.user_id is not None:
                chat_map[chat.user_id].append(chat)
        return [chat_map.get(user_id, []) for user_id in user_ids]

    async def _load_chat_room_members(
        self, user_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        stmt = select(ChatRoomMemberModel).where(
            ChatRoomMemberModel.user_id.in_(user_ids)
        )
        result = await db.execute(stmt)
        members = result.scalars().all()
        member_map: dict[int, List[ChatRoomMemberModel]] = {
            user_id: [] for user_id in user_ids
        }
        for member in members:
            if member.user_id is not None:
                member_map[member.user_id].append(member)
        return [member_map.get(user_id, []) for user_id in user_ids]
