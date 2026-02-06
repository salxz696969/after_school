from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import get_chat_columns, get_chat_room_member_columns


class ChatRoomLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ChatModel]]
        ] = DataLoader(load_fn=self._load_chats)
        self.member_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ChatRoomMemberModel]]
        ] = DataLoader(load_fn=self._load_members)

    async def _load_chats(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[ChatModel]]]:
        try:
            chat_room_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_columns(list(fields))
            if "chat_room_id" not in fields:
                column_dict["chat_room_id"] = ChatRoomMemberModel.chat_room_id
            stmt = select(*column_dict.values()).where(ChatModel.chat_room_id.in_(chat_room_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            chats = result.mappings().all()
            return [
                [ChatModel(**chat) for chat in chats if chat["chat_room_id"] == room_id]
                for room_id in chat_room_ids
            ]
        except Exception as e:
            raise e

    async def _load_members(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        try:
            chat_room_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_room_member_columns(list(fields))
            if "chat_room_id" not in fields:
                column_dict["chat_room_id"] = ChatRoomMemberModel.chat_room_id
            stmt = select(*column_dict.values()).where(ChatRoomMemberModel.chat_room_id.in_(chat_room_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            members = result.mappings().all()
            return [
                [
                    ChatRoomMemberModel(**member)
                    for member in members
                    if member["chat_room_id"] == room_id
                ]
                for room_id in chat_room_ids
            ]
        except Exception as e:
            raise e
