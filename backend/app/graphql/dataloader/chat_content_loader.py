from typing import List, Optional
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from app.models.chat_content_model import ChatContentModel
from app.models.chat_model import ChatModel
from app.models.media_model import MediaModel
from sqlalchemy.ext.asyncio import AsyncSession


class ChatContentLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.chat_loader: DataLoader[int, Optional[ChatModel]] = DataLoader(
            load_fn=lambda ids: self._load_chat_by(ids, db)
        )
        self.media_loader: DataLoader[int, Optional[List[MediaModel]]] = DataLoader(
            load_fn=lambda ids: self._load_medias_by(ids, db)
        )

    async def _load_chat_by(
        self, chat_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[ChatModel]]:
        stmt = (
            select(ChatModel)
            .join(ChatContentModel)
            .where(ChatContentModel.id.in_(chat_content_ids))
        )
        result = await db.execute(stmt)
        chats = result.scalars().all()
        chat_map = {chat.id: chat for chat in chats}
        return [chat_map.get(chat_content) for chat_content in chat_content_ids]

    async def _load_medias_by(
        self, chat_content_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[MediaModel]]]:
        stmt = select(MediaModel).where(
            MediaModel.chat_content_id.in_(chat_content_ids)
        )
        result = await db.execute(stmt)
        medias = result.scalars().all()
        media_map: dict[int, List[MediaModel]] = {
            chat_content_id: [] for chat_content_id in chat_content_ids
        }
        for media in medias:
            if media.chat_content_id is not None:
                media_map[media.chat_content_id].append(media)
        return [
            media_map.get(chat_content_id, []) for chat_content_id in chat_content_ids
        ]
