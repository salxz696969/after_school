from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_model import ChatModel
from app.models.chat_room_model import ChatRoomModel
from app.models.user_model import UserModel
from app.models.chat_content_model import ChatContentModel
from strawberry.dataloader import DataLoader


class ChatLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_room_loader: DataLoader[int, Optional[ChatRoomModel]] = DataLoader(
            load_fn=lambda ids: self._load_chat_rooms(ids, db)
        )
        self.user_loader: DataLoader[int, Optional[UserModel]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )
        self.content_loader: DataLoader[int, Optional[List[ChatContentModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_contents(ids, db))
        )

    async def _load_chat_rooms(
        self, chat_ids: List[int], db: AsyncSession
    ) -> List[Optional[ChatRoomModel]]:
        stmt = select(ChatRoomModel).join(ChatModel).where(ChatModel.id.in_(chat_ids))
        result = await db.execute(stmt)
        chat_rooms = result.scalars().all()
        chat_room_map = {chat_room.id: chat_room for chat_room in chat_rooms}
        return [chat_room_map.get(chat_id) for chat_id in chat_ids]

    async def _load_users(
        self, chat_ids: List[int], db: AsyncSession
    ) -> List[Optional[UserModel]]:
        stmt = select(UserModel).join(ChatModel).where(ChatModel.id.in_(chat_ids))
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map = {user.id: user for user in users}
        return [user_map.get(chat_id) for chat_id in chat_ids]

    async def _load_contents(
        self, chat_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ChatContentModel]]]:
        stmt = select(ChatContentModel).where(ChatContentModel.chat_id.in_(chat_ids))
        result = await db.execute(stmt)
        contents = result.scalars().all()
        content_map: dict[int, List[ChatContentModel]] = {
            chat_id: [] for chat_id in chat_ids
        }
        for content in contents:
            if content.chat_id is not None:
                content_map[content.chat_id].append(content)
        return [content_map.get(chat_id, []) for chat_id in chat_ids]
