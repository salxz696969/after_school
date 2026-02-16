import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.announcement_model import AnnouncementModel
from app.db.assignment_model import AssignmentModel
from app.db.assignment_reply_model import AssignmentReplyModel
from app.db.chat_model import ChatModel
from app.db.chat_room_member_model import ChatRoomMemberModel
from app.db.class_model import ClassModel
from app.db.user_model import UserModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class UserLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._class_fields: List[str] | None = None
        self._assignment_fields: List[str] | None = None
        self._assignment_reply_fields: List[str] | None = None
        self._announcement_fields: List[str] | None = None
        self._chat_fields: List[str] | None = None
        self._chat_room_member_fields: List[str] | None = None
        self.class_loader: DataLoader[int, Optional[ClassModel]] | None = None
        self.assignment_loader: (
            DataLoader[int, Optional[List[AssignmentModel]]] | None
        ) = None
        self.assignment_reply_loader: (
            DataLoader[int, Optional[List[AssignmentReplyModel]]] | None
        ) = None
        self.announcement_loader: (
            DataLoader[int, Optional[List[AnnouncementModel]]] | None
        ) = None
        self.chat_loader: DataLoader[int, Optional[List[ChatModel]]] | None = None
        self.chat_room_member_loader: (
            DataLoader[int, Optional[List[ChatRoomMemberModel]]] | None
        ) = None

    def create_class_loader(self, fields: List[str]) -> None:
        self._class_fields = fields
        self.class_loader = DataLoader(load_fn=self._load_classes)

    def create_assignment_loader(self, fields: List[str]) -> None:
        self._assignment_fields = fields
        self.assignment_loader = DataLoader(load_fn=self._load_assignments)

    def create_assignment_reply_loader(self, fields: List[str]) -> None:
        self._assignment_reply_fields = fields
        self.assignment_reply_loader = DataLoader(load_fn=self._load_assignment_replies)

    def create_announcement_loader(self, fields: List[str]) -> None:
        self._announcement_fields = fields
        self.announcement_loader = DataLoader(load_fn=self._load_announcements)

    def create_chat_loader(self, fields: List[str]) -> None:
        self._chat_fields = fields
        self.chat_loader = DataLoader(load_fn=self._load_chats)

    def create_chat_room_member_loader(self, fields: List[str]) -> None:
        self._chat_room_member_fields = fields
        self.chat_room_member_loader = DataLoader(load_fn=self._load_chat_room_members)

    async def _load_classes(self, keys: List[int]) -> List[Optional[ClassModel]]:
        try:
            if not self._class_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_class_columns(list(self._class_fields))
            stmt = select(*column_list).join(UserModel, UserModel.class_id == ClassModel.id).where(UserModel.id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                classes = result.mappings().all()  # type: ignore
                return [ClassModel(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading classes: {e}")
            raise HTTPException(status_code=500, detail="Failed to load classes")

    async def _load_assignments(
        self, keys: List[int]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            if not self._assignment_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_assignment_columns(
                list(self._assignment_fields)
            )
            if "userId" not in self._assignment_fields:
                column_list.append(AssignmentModel.user_id)
            stmt = select(*column_list).where(AssignmentModel.user_id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignments = result.mappings().all()  # type: ignore
                return [
                    [
                        AssignmentModel(**assignment)
                        for assignment in assignments  # type: ignore
                        if assignment["user_id"] == user_id
                    ]
                    for user_id in user_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to load assignments")

    async def _load_assignment_replies(
        self, keys: List[int]
    ) -> List[Optional[List[AssignmentReplyModel]]]:
        try:
            if not self._assignment_reply_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_assignment_reply_columns(
                list(self._assignment_reply_fields)
            )
            if "userId" not in self._assignment_reply_fields:
                column_list.append(AssignmentReplyModel.user_id)
            stmt = select(*column_list).where(AssignmentReplyModel.user_id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                replies = result.mappings().all()  # type: ignore
                return [
                    [
                        AssignmentReplyModel(**reply)
                        for reply in replies  # type: ignore
                        if reply["user_id"] == user_id
                    ]
                    for user_id in user_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading assignment replies: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load assignment replies"
            )

    async def _load_announcements(
        self, keys: List[int]
    ) -> List[Optional[List[AnnouncementModel]]]:
        try:
            if not self._announcement_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_announcement_columns(
                list(self._announcement_fields)
            )
            if "userId" not in self._announcement_fields:
                column_list.append(AnnouncementModel.user_id)
            stmt = select(*column_list).where(AnnouncementModel.user_id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                announcements = result.mappings().all()  # type: ignore
                return [
                    [
                        AnnouncementModel(**announcement)
                        for announcement in announcements  # type: ignore
                        if announcement["user_id"] == user_id
                    ]
                    for user_id in user_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading announcements: {e}")
            raise HTTPException(status_code=500, detail="Failed to load announcements")

    async def _load_chats(self, keys: List[int]) -> List[Optional[List[ChatModel]]]:
        try:
            if not self._chat_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_chat_columns(list(self._chat_fields))
            if "userId" not in self._chat_fields:
                column_list.append(ChatModel.user_id)
            stmt = select(*column_list).where(ChatModel.user_id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chats = result.mappings().all()  # type: ignore
                return [
                    [ChatModel(**chat) for chat in chats if chat["user_id"] == user_id]  # type: ignore
                    for user_id in user_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading chats: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chats")

    async def _load_chat_room_members(
        self, keys: List[int]
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        try:
            if not self._chat_room_member_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            user_ids = keys
            column_list = ColumnGetter.get_chat_room_member_columns(
                list(self._chat_room_member_fields)
            )
            if "userId" not in self._chat_room_member_fields:
                column_list.append(ChatRoomMemberModel.user_id)
            stmt = select(*column_list).where(ChatRoomMemberModel.user_id.in_(user_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                members = result.mappings().all()  # type: ignore
                return [
                    [
                        ChatRoomMemberModel(**member)
                        for member in members  # type: ignore
                        if member["user_id"] == user_id
                    ]
                    for user_id in user_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading chat room members: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load chat room members"
            )
