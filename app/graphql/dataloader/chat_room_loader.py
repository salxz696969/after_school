import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.chat_model import ChatModel
from app.db.chat_room_member_model import ChatRoomMemberModel
from strawberry.dataloader import DataLoader
from app.utils.get_column import ColumnGetter
from app.core.database import AsyncSessionLocal


class ChatRoomLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._chat_fields: List[str] | None = None
        self._member_fields: List[str] | None = None
        self.chat_loader: DataLoader[int, Optional[List[ChatModel]]] | None = None
        self.member_loader: (
            DataLoader[int, Optional[List[ChatRoomMemberModel]]] | None
        ) = None

    def create_chat_loader(self, fields: List[str]) -> None:
        self._chat_fields = fields
        self.chat_loader = DataLoader(load_fn=self._load_chats)

    def create_member_loader(self, fields: List[str]) -> None:
        self._member_fields = fields
        self.member_loader = DataLoader(load_fn=self._load_members)

    async def _load_chats(self, keys: List[int]) -> List[Optional[List[ChatModel]]]:
        try:
            if not self._chat_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_room_ids = keys
            column_list = ColumnGetter.get_chat_columns(list(self._chat_fields))
            if "chatRoomId" not in self._chat_fields:
                column_list.append(ChatModel.chat_room_id)
            stmt = select(*column_list).where(ChatModel.chat_room_id.in_(chat_room_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chats = result.mappings().all()  # type: ignore
                return [
                    [
                        ChatModel(**chat)
                        for chat in chats  # type: ignore
                        if chat["chat_room_id"] == room_id
                    ]
                    for room_id in chat_room_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading chats: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chats")

    async def _load_members(
        self, keys: List[int]
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        try:
            if not self._member_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_room_ids = keys
            column_list = ColumnGetter.get_chat_room_member_columns(
                list(self._member_fields)
            )
            if "chatRoomId" not in self._member_fields:
                column_list.append(ChatRoomMemberModel.chat_room_id)
            stmt = select(*column_list).where(ChatRoomMemberModel.chat_room_id.in_(chat_room_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                members = result.mappings().all()  # type: ignore
                return [
                    [
                        ChatRoomMemberModel(**member)
                        for member in members  # type: ignore
                        if member["chat_room_id"] == room_id
                    ]
                    for room_id in chat_room_ids
                ]
        except Exception as e:
            logging.exception(f"Error loading chat room members: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to load chat room members"
            )
