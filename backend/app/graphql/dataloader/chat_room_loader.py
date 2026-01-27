from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel
from strawberry.dataloader import DataLoader


class ChatRoomLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_loader: DataLoader[int, Optional[List[ChatModel]]] = DataLoader(
            load_fn=lambda ids: self._load_chats(ids, db)
        )
        self.member_loader: DataLoader[int, Optional[List[ChatRoomMemberModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_members(ids, db))
        )

    async def _load_chats(
        self, chat_room_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ChatModel]]]:
        stmt = select(ChatModel).where(ChatModel.chat_room_id.in_(chat_room_ids))
        result = await db.execute(stmt)
        chats = result.scalars().all()
        chat_map: dict[int, List[ChatModel]] = {
            room_id: [] for room_id in chat_room_ids
        }
        for chat in chats:
            if chat.chat_room_id is not None:
                chat_map[chat.chat_room_id].append(chat)
        return [chat_map.get(room_id, []) for room_id in chat_room_ids]

    async def _load_members(
        self, chat_room_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ChatRoomMemberModel]]]:
        stmt = select(ChatRoomMemberModel).where(
            ChatRoomMemberModel.chat_room_id.in_(chat_room_ids)
        )
        result = await db.execute(stmt)
        members = result.scalars().all()
        member_map: dict[int, List[ChatRoomMemberModel]] = {
            room_id: [] for room_id in chat_room_ids
        }
        for member in members:
            if member.chat_room_id is not None:
                member_map[member.chat_room_id].append(member)
        return [member_map.get(room_id, []) for room_id in chat_room_ids]
