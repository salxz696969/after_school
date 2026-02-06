from typing import List, Optional
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from app.models.chat_content_model import ChatContentModel
from app.models.chat_model import ChatModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.get_column import get_chat_columns, get_media_columns


class ChatContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[ChatModel]
        ] = DataLoader(load_fn=self._load_chat_by)
        self.media_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[MediaModel]]
        ] = DataLoader(load_fn=self._load_medias_by)

    async def _load_chat_by(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[ChatModel]]:
        try:
            fields = keys[0][1]
            chat_content_ids = [key[0] for key in keys]
            column_dict = get_chat_columns(list(fields))
            stmt = select(*column_dict.values()).join(ChatContentModel).where(ChatContentModel.id.in_(chat_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            chats = result.mappings().all()
            return [ChatModel(**chat) for chat in chats]  # type: ignore
        except Exception as e:
            raise e

    async def _load_medias_by(
        self, keys: List[tuple[int, tuple[str, ...]]]
    ) -> List[Optional[List[MediaModel]]]:
        try:
            chat_content_ids = [key[0] for key in keys]
            fields = keys[0][1]
            column_dict = get_media_columns(list(fields))
            if "chat_content_id" not in fields:
                column_dict["chat_content_id"] = ChatContentModel.id
            stmt = select(*column_dict.values()).where(MediaModel.chat_content_id.in_(chat_content_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            medias = result.mappings().all()
            return [MediaModel(**media) for media in medias]  # type: ignore
        except Exception as e:
            raise e
