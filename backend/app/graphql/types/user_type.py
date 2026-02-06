from __future__ import annotations
import strawberry
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, List
from app.utils import extract_fields
from app.core.context import Context

if TYPE_CHECKING:
    from .assignment_reply_type import AssignmentReplyType
    from .assignment_type import AssignmentType
    from .chat_room_member_type import ChatRoomMemberType
    from .chat_type import ChatType
    from .class_type import ClassType
    from .announcement_type import AnnouncementType


@strawberry.type
class UserType:
    id: int
    username: str | None = None
    email: str | None = None
    password: str | None = None
    avatar_url: str | None = None
    class_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    def class_(self, info: strawberry.Info[Context]) -> Annotated[
        "ClassType",
        strawberry.lazy("app.graphql.types.class_type"),
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.class_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def assignments(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentType",
            strawberry.lazy("app.graphql.types.assignment_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.assignment_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def assignment_replies(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AssignmentReplyType",
            strawberry.lazy("app.graphql.types.assignment_reply_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.assignment_reply_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def announcements(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "AnnouncementType",
            strawberry.lazy("app.graphql.types.announcement_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.announcement_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def chats(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ChatType",
            strawberry.lazy("app.graphql.types.chat_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.chat_loader.load((self.id, tuple(fields)))  # type: ignore

    @strawberry.field
    def chat_room_members(self, info: strawberry.Info[Context]) -> List[
        Annotated[
            "ChatRoomMemberType",
            strawberry.lazy("app.graphql.types.chat_room_member_type"),
        ]
    ]:
        fields = extract_fields(info)
        return info.context.user_loader.chat_room_member_loader.load((self.id, tuple(fields)))  # type: ignore
