from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_model import ChatModel
from app.models.chat_room_model import ChatRoomModel
from app.models.user_model import UserModel
from app.models.chat_content_model import ChatContentModel
from strawberry.dataloader import DataLoader

from app.utils.get_column import (
    get_chat_content_columns,
    get_chat_room_columns,
    get_user_columns,
)


class ChatLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_room_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ChatRoomModel]
        ] = DataLoader(load_fn=self._load_chat_rooms)
        self.user_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[UserModel]
        ] = DataLoader(load_fn=self._load_users)
        self.content_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ChatContentModel]]
        ] = DataLoader(load_fn=self._load_contents)

    async def _load_chat_rooms(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ChatRoomModel]]:
        try:
            chat_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_room_columns(list(fields))
            if "chat_id" not in fields:
                column_dict["chat_id"] = ChatModel.id
            stmt = select(*column_dict.values()).join(ChatModel).where(ChatModel.id.in_(chat_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            chat_rooms = result.mappings().all()
            return [ChatRoomModel(**chat_room) for chat_room in chat_rooms]  # type: ignore
        except Exception as e:
            raise e

    async def _load_users(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[UserModel]]:
        try:
            chat_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_user_columns(list(fields))
            if "chat_id" not in fields:
                column_dict["chat_id"] = ChatModel.id
            stmt = select(*column_dict.values()).join(ChatModel).where(ChatModel.id.in_(chat_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            raise e

    async def _load_contents(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ChatContentModel]]:
        try:
            chat_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_chat_content_columns(list(fields))
            if "chat_id" not in fields:
                column_dict["chat_id"] = ChatModel.id
            stmt = select(*column_dict.values()).where(ChatContentModel.chat_id.in_(chat_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            contents = result.mappings().all()
            return [ChatContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            raise e
