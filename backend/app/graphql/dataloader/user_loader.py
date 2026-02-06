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

from app.utils.get_column import (
    get_announcement_columns,
    get_assignment_columns,
    get_assignment_reply_columns,
    get_chat_columns,
    get_chat_room_member_columns,
    get_class_columns,
)


class UserLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.class_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ClassModel]
        ] = DataLoader(load_fn=self._load_classes)
        self.assignment_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AssignmentModel]]
        ] = DataLoader(load_fn=self._load_assignments)
        self.assignment_reply_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AssignmentReplyModel]]
        ] = DataLoader(load_fn=self._load_assignment_replies)
        self.announcement_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AnnouncementModel]]
        ] = DataLoader(load_fn=self._load_announcements)
        self.chat_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ChatModel]]
        ] = DataLoader(load_fn=self._load_chats)
        self.chat_room_member_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ChatRoomMemberModel]]
        ] = DataLoader(load_fn=self._load_chat_room_members)

    async def _load_classes(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ClassModel]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_class_columns(list(fields))
            stmt = select(*column_dict.values()).join(UserModel).where(UserModel.id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            classes = result.mappings().all()
            return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            raise e

    async def _load_assignments(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_columns(list(fields))
            if "user_id" not in fields:
                column_dict["user_id"] = UserModel.id
            stmt = select(*column_dict.values()).where(AssignmentModel.user_id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignments = result.mappings().all()
            return [
                [
                    AssignmentModel(**assignment)
                    for assignment in assignments
                    if assignment["user_id"] == user_id
                ]
                for user_id in user_ids
            ]
        except Exception as e:
            raise e

    async def _load_assignment_replies(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_assignment_reply_columns(list(fields))
            if "user" not in fields:
                column_dict["assignment_reply_id"] = UserModel.id
            stmt = select(*column_dict.values()).where(AssignmentReplyModel.user_id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            replies = result.mappings().all()
            return [
                [
                    AssignmentReplyModel(**reply)
                    for reply in replies
                    if reply["user_id"] == user_id
                ]
                for user_id in user_ids
            ]
        except Exception as e:
            raise e

    async def _load_announcements(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[AnnouncementModel]]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_announcement_columns(list(fields))
            if "user_id" not in fields:
                column_dict["user_id"] = UserModel.id
            stmt = select(*column_dict.values()).where(AnnouncementModel.user_id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            announcements = result.mappings().all()
            return [
                [
                    AnnouncementModel(**announcement)
                    for announcement in announcements
                    if announcement["user_id"] == user_id
                ]
                for user_id in user_ids
            ]
        except Exception as e:
            raise e

    async def _load_chats(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[ChatModel]]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_columns(list(fields))
            if "user_id" not in fields:
                column_dict["user_id"] = UserModel.id
            stmt = select(*column_dict.values()).where(ChatModel.user_id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            chats = result.mappings().all()
            return [
                [ChatModel(**chat) for chat in chats if chat["user_id"] == user_id]
                for user_id in user_ids
            ]
        except Exception as e:
            raise e

    async def _load_chat_room_members(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        try:
            user_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_room_member_columns(list(fields))
            if "user_id" not in fields:
                column_dict["user_id"] = UserModel.id
            stmt = select(*column_dict.values()).where(ChatRoomMemberModel.user_id.in_(user_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            members = result.mappings().all()
            return [
                [
                    ChatRoomMemberModel(**member)
                    for member in members
                    if member["user_id"] == user_id
                ]
                for user_id in user_ids
            ]
        except Exception as e:
            raise e
