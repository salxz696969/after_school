import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.db.chat_model import ChatModel
from app.db.chat_room_model import ChatRoomModel
from app.db.user_model import UserModel
from app.db.chat_content_model import ChatContentModel
from strawberry.dataloader import DataLoader
from app.core.database import AsyncSessionLocal
from app.utils.get_column import ColumnGetter


class ChatLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._chat_room_fields: List[str] | None = None
        self._user_fields: List[str] | None = None
        self._content_fields: List[str] | None = None
        self.chat_room_loader: DataLoader[int, Optional[ChatRoomModel]] | None = None
        self.user_loader: DataLoader[int, Optional[UserModel]] | None = None
        self.content_loader: DataLoader[int, Optional[ChatContentModel]] | None = None

    def create_chat_room_loader(self, fields: List[str]) -> None:
        self._chat_room_fields = fields
        self.chat_room_loader = DataLoader(load_fn=self._load_chat_rooms)

    def create_user_loader(self, fields: List[str]) -> None:
        self._user_fields = fields
        self.user_loader = DataLoader(load_fn=self._load_users)

    def create_content_loader(self, fields: List[str]) -> None:
        self._content_fields = fields
        self.content_loader = DataLoader(load_fn=self._load_contents)

    async def _load_chat_rooms(self, keys: List[int]) -> List[Optional[ChatRoomModel]]:
        try:
            if not self._chat_room_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_ids = keys
            column_list = ColumnGetter.get_chat_room_columns(
                list(self._chat_room_fields)
            )
            stmt = select(*column_list).join(ChatModel, ChatModel.chat_room_id == ChatRoomModel.id).where(ChatModel.id.in_(chat_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chat_rooms = result.mappings().all()  # type: ignore
                return [ChatRoomModel(**chat_room) for chat_room in chat_rooms]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading chat rooms: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chat rooms")

    async def _load_users(self, keys: List[int]) -> List[Optional[UserModel]]:
        try:
            if not self._user_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_ids = keys
            column_list = ColumnGetter.get_user_columns(list(self._user_fields))
            stmt = select(*column_list).join(ChatModel, ChatModel.user_id == UserModel.id).where(ChatModel.id.in_(chat_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                return [UserModel(**user) for user in users]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            raise HTTPException(status_code=500, detail="Failed to load users")

    async def _load_contents(self, keys: List[int]) -> List[Optional[ChatContentModel]]:
        try:
            if not self._content_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_ids = keys
            column_list = ColumnGetter.get_chat_content_columns(
                list(self._content_fields)
            )
            if "chatId" not in self._content_fields:
                column_list.append(ChatContentModel.chat_id)
            stmt = select(*column_list).where(ChatContentModel.chat_id.in_(chat_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                contents = result.mappings().all()  # type: ignore
                return [ChatContentModel(**content) for content in contents]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading chat contents: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chat contents")
