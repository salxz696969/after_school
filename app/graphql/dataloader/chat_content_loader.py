import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from app.db.chat_content_model import ChatContentModel
from app.db.chat_model import ChatModel
from app.db.media_model import MediaModel
from app.utils.get_column import ColumnGetter
from app.core.database import AsyncSessionLocal


class ChatContentLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._chat_fields: List[str] | None = None
        self._media_fields: List[str] | None = None
        self.chat_loader: DataLoader[int, Optional[ChatModel]] | None = None
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] | None = None

    def create_chat_loader(self, fields: List[str]) -> None:
        self._chat_fields = fields
        self.chat_loader = DataLoader(load_fn=self._load_chat)

    def create_media_loader(self, fields: List[str]) -> None:
        self._media_fields = fields
        self.media_loader = DataLoader(load_fn=self._load_medias)

    async def _load_chat(self, keys: List[int]) -> List[Optional[ChatModel]]:
        try:
            if not self._chat_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_content_ids = keys
            column_list = ColumnGetter.get_chat_columns(list(self._chat_fields))
            stmt = select(*column_list).join(ChatContentModel, ChatContentModel.chat_id == ChatModel.id).where(ChatContentModel.id.in_(chat_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                chats = result.mappings().all()  # type: ignore
                return [ChatModel(**chat) for chat in chats]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading chats: {e}")
            raise HTTPException(status_code=500, detail="Failed to load chats")

    async def _load_medias(self, keys: List[int]) -> List[Optional[List[MediaModel]]]:
        try:
            if not self._media_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            chat_content_ids = keys
            column_list = ColumnGetter.get_media_columns(list(self._media_fields))
            if "chatContentId" not in self._media_fields:
                column_list.append(MediaModel.chat_content_id)
            stmt = select(*column_list).where(MediaModel.chat_content_id.in_(chat_content_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                medias = result.mappings().all()  # type: ignore
                return [
                    [
                        MediaModel(**media)
                        for media in medias  # type: ignore
                        if media["chat_content_id"] == content_id
                    ]
                    for content_id in chat_content_ids
                ]  # type: ignore
        except Exception as e:
            logging.exception(f"Error loading medias: {e}")
            raise HTTPException(status_code=500, detail="Failed to load medias")
