from strawberry.types import Info
from strawberry.types.nodes import SelectedField

valid_fields = {
    "user", "users", "subject", "subjects", "scheduleContent", "scheduleContents", "schedule",
    "schedules", "media", "medias", "class_", "chatRoom", "chatRooms", "chatRoomMember",
    "chatRoomMembers", "chat", "chats", "chatContent", "chatContents", "assignmentReply",
    "assignmentReplies", "assignmentReplyContent", "assignmentReplyContents", "assignment",
    "assignments", "assignmentContent", "assignmentContents", "announcementContent",
    "announcementContents", "announcement", "announcements"
}

def validate_fields(info: Info, parent_field: str) -> bool:
    seen_valid: set[str] = set()
    stack: list[list[SelectedField]] = [info.selected_fields]  # type: ignore
    while stack:
        selections = stack.pop()
        for field in selections:
            if field.name == parent_field:
                return False
            if field.name in valid_fields:
                if field.name in seen_valid:
                    return False
                seen_valid.add(field.name)
            if field.selections:
                stack.append(field.selections)  # type: ignore

    return True