from __future__ import annotations
import strawberry
from datetime import datetime
from typing import Annotated
from typing import TYPE_CHECKING
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .chat_room_type import ChatRoomType
    from .user_type import UserType
    from .chat_content_type import ChatContentType


@strawberry.type
class ChatType:
    id: int
    chat_room_id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def chat_room(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatRoomType",
        strawberry.lazy("app.graphql.types.chat_room_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.chat_loader.chat_room_loader:  # type: ignore
            info.context.chat_loader.create_chat_room_loader(fields)  # type: ignore
        return info.context.chat_loader.chat_room_loader.load(self.chat_room_id)  # type: ignore

    @strawberry.field
    def user(self, info: strawberry.Info[Context]) -> Annotated[
        "UserType",
        strawberry.lazy("app.graphql.types.user_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.chat_loader.user_loader:  # type: ignore
            info.context.chat_loader.create_user_loader(fields)  # type: ignore
        return info.context.chat_loader.user_loader.load(self.user_id)  # type: ignore

    @strawberry.field
    def chat_content(self, info: strawberry.Info[Context]) -> Annotated[
        "ChatContentType",
        strawberry.lazy("app.graphql.types.chat_content_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.chat_loader.content_loader:  # type: ignore
            info.context.chat_loader.create_content_loader(fields)  # type: ignore
        return info.context.chat_loader.content_loader.load(self.id)  # type: ignore
