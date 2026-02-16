from __future__ import annotations
from typing import TYPE_CHECKING, Annotated
import strawberry
from app.core.context import Context
from datetime import datetime

from app.utils import extract_fields

if TYPE_CHECKING:
    from .chat_room_type import ChatRoomType
    from .user_type import UserType


@strawberry.type
class ChatRoomMemberType:
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
        if not info.context.chat_room_member_loader.chat_room_loader:  # type: ignore
            info.context.chat_room_member_loader.create_chat_room_loader(fields)  # type: ignore
        return info.context.chat_room_member_loader.chat_room_loader.load(self.id)  # type: ignore

    @strawberry.field
    def user(self, info: strawberry.Info[Context]) -> Annotated[
        "UserType",
        strawberry.lazy("app.graphql.types.user_type"),
    ]:
        fields = extract_fields(info)
        if not info.context.chat_room_member_loader.user_loader:  # type: ignore
            info.context.chat_room_member_loader.create_user_loader(fields)  # type: ignore
        return info.context.chat_room_member_loader.user_loader.load(self.id)  # type: ignore
