from __future__ import annotations
import enum
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, List, Annotated
from app.core.context import Context
from app.utils import extract_fields

if TYPE_CHECKING:
    from .chat_type import ChatType
    from .chat_room_member_type import ChatRoomMemberType


@strawberry.enum
class ChatRoomTypeEnum(enum.Enum):
    GROUP_CHAT = "group_chat"
    DIRECT_MESSAGE = "direct_message"


@strawberry.type
class ChatRoomType:
    id: int
    chat_room_type: ChatRoomTypeEnum | None = None
    chat_room_name: str | None = None
    avatar_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def chats(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ChatType",
            strawberry.lazy("app.graphql.types.chat_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.chat_room_loader.chats_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def members(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ChatRoomMemberType",
            strawberry.lazy("app.graphql.types.chat_room_member_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.chat_room_loader.members_loader.load((self.id, tuple(fields)))  # type: ignore
