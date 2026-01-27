from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_room_member_model import ChatRoomMemberModel
from app.models.chat_room_model import ChatRoomModel
from app.models.user_model import UserModel
from strawberry.dataloader import DataLoader


class ChatRoomMemberLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_room_loader: DataLoader[int, Optional[ChatRoomModel]] = DataLoader(
            load_fn=lambda ids: self._load_chat_rooms(ids, db)
        )
        self.user_loader: DataLoader[int, Optional[UserModel]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )

    async def _load_chat_rooms(
        self, member_ids: List[int], db: AsyncSession
    ) -> List[Optional[ChatRoomModel]]:
        stmt = (
            select(ChatRoomModel)
            .join(ChatRoomMemberModel)
            .where(ChatRoomMemberModel.id.in_(member_ids))
        )
        result = await db.execute(stmt)
        chat_rooms = result.scalars().all()
        chat_room_map = {chat_room.id: chat_room for chat_room in chat_rooms}
        return [chat_room_map.get(member_id) for member_id in member_ids]

    async def _load_users(
        self, member_ids: List[int], db: AsyncSession
    ) -> List[Optional[UserModel]]:
        stmt = (
            select(UserModel)
            .join(ChatRoomMemberModel)
            .where(ChatRoomMemberModel.id.in_(member_ids))
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map = {user.id: user for user in users}
        return [user_map.get(member_id) for member_id in member_ids]
