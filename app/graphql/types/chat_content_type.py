from __future__ import annotations
import strawberry
from datetime import datetime
from app.core.context import Context
from typing import TYPE_CHECKING, Annotated, List

from app.utils import extract_fields

if TYPE_CHECKING:
    from .chat_type import ChatType
    from .media_type import MediaType


@strawberry.type
class ChatContentType:
    id: int
    text: str | None = None
    chat_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def chat(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatType",
        strawberry.lazy("app.graphql.types.chat_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.chat_content_loader.chat_loader:  # type: ignore
            info.context.chat_content_loader.create_chat_loader(fields)  # type: ignore
        return info.context.chat_content_loader.chat_loader.load(self.id)  # type: ignore

    @strawberry.field
    def medias(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "MediaType",
            strawberry.lazy("app.graphql.types.media_type"),
        ]
    ]:
        fields = extract_fields(info)
        if not info.context.chat_content_loader.media_loader:  # type: ignore
            info.context.chat_content_loader.create_media_loader(fields)  # type: ignore
        return info.context.chat_content_loader.media_loader.load(self.id)  # type: ignore
