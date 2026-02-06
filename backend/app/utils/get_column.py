from app.models.class_model import ClassModel
from app.models.announcement_content_model import AnnouncementContentModel
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_content_model import AssignmentContentModel
from app.models.assignment_model import AssignmentModel
from app.models.assignment_reply_content_model import AssignmentReplyContentModel
from app.models.assignment_reply_model import AssignmentReplyModel
from app.models.chat_content_model import ChatContentModel
from app.models.chat_model import ChatModel
from app.models.chat_room_member_model import ChatRoomMemberModel
from app.models.chat_room_model import ChatRoomModel
from app.models.media_model import MediaModel
from app.models.schedule_content_model import ScheduleContentModel
from app.models.schedule_model import ScheduleModel
from app.models.subject_model import SubjectModel
from app.models.user_model import UserModel


def get_class_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ClassModel.id,
        "speciality": ClassModel.speciality,
        "major": ClassModel.major,
        "groupName": ClassModel.group_name,
        "generation": ClassModel.generation,
        "createdAt": ClassModel.created_at,
        "updatedAt": ClassModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ClassModel.id
    return fields


def get_announcement_content_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AnnouncementContentModel.id,
        "text": AnnouncementContentModel.text,
        "announcementId": AnnouncementContentModel.announcement_id,
        "createdAt": AnnouncementContentModel.created_at,
        "updatedAt": AnnouncementContentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AnnouncementContentModel.id
    return fields


def get_announcement_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AnnouncementModel.id,
        "userId": AnnouncementModel.user_id,
        "classId": AnnouncementModel.class_id,
        "type": AnnouncementModel.type,
        "createdAt": AnnouncementModel.created_at,
        "updatedAt": AnnouncementModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AnnouncementModel.id
    return fields


def get_assignment_content_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AssignmentContentModel.id,
        "text": AssignmentContentModel.text,
        "assignmentId": AssignmentContentModel.assignment_id,
        "createdAt": AssignmentContentModel.created_at,
        "updatedAt": AssignmentContentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AssignmentContentModel.id
    return fields


def get_assignment_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AssignmentModel.id,
        "userId": AssignmentModel.user_id,
        "subjectId": AssignmentModel.subject_id,
        "classId": AssignmentModel.class_id,
        "createdAt": AssignmentModel.created_at,
        "updatedAt": AssignmentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AssignmentModel.id
    return fields


def get_assignment_reply_content_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AssignmentReplyContentModel.id,
        "text": AssignmentReplyContentModel.text,
        "assignmentReplyId": AssignmentReplyContentModel.assignment_reply_id,
        "createdAt": AssignmentReplyContentModel.created_at,
        "updatedAt": AssignmentReplyContentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AssignmentReplyContentModel.id
    return fields


def get_assignment_reply_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": AssignmentReplyModel.id,
        "assignmentId": AssignmentReplyModel.assignment_id,
        "userId": AssignmentReplyModel.user_id,
        "upVote": AssignmentReplyModel.up_vote,
        "downVote": AssignmentReplyModel.down_vote,
        "createdAt": AssignmentReplyModel.created_at,
        "updatedAt": AssignmentReplyModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = AssignmentReplyModel.id
    return fields


def get_chat_content_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ChatContentModel.id,
        "text": ChatContentModel.text,
        "chatId": ChatContentModel.chat_id,
        "createdAt": ChatContentModel.created_at,
        "updatedAt": ChatContentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ChatContentModel.id
    return fields


def get_chat_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ChatModel.id,
        "chatRoomId": ChatModel.chat_room_id,
        "userId": ChatModel.user_id,
        "createdAt": ChatModel.created_at,
        "updatedAt": ChatModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ChatModel.id
    return fields


def get_chat_room_member_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ChatRoomMemberModel.id,
        "chatRoomId": ChatRoomMemberModel.chat_room_id,
        "userId": ChatRoomMemberModel.user_id,
        "createdAt": ChatRoomMemberModel.created_at,
        "updatedAt": ChatRoomMemberModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ChatRoomMemberModel.id
    return fields


def get_chat_room_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ChatRoomModel.id,
        "chat_room_type": ChatRoomModel.chat_room_type,
        "chatRoomName": ChatRoomModel.chat_room_name,
        "avatarUrl": ChatRoomModel.avatar_url,
        "createdAt": ChatRoomModel.created_at,
        "updatedAt": ChatRoomModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ChatRoomModel.id
    return fields


def get_media_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": MediaModel.id,
        "url": MediaModel.url,
        "chatContentId": MediaModel.chat_content_id,
        "scheduleContentId": MediaModel.schedule_content_id,
        "announcementContentId": MediaModel.announcement_content_id,
        "assignmentContentId": MediaModel.assignment_content_id,
        "assignmentReplyContentId": MediaModel.assignment_reply_content_id,
        "createdAt": MediaModel.created_at,
        "updatedAt": MediaModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = MediaModel.id
    return fields


def get_schedule_content_columns(
    field: list[str],
) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ScheduleContentModel.id,
        "text": ScheduleContentModel.text,
        "scheduleId": ScheduleContentModel.schedule_id,
        "createdAt": ScheduleContentModel.created_at,
        "updatedAt": ScheduleContentModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ScheduleContentModel.id
    return fields


def get_schedule_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": ScheduleModel.id,
        "classId": ScheduleModel.class_id,
        "createdAt": ScheduleModel.created_at,
        "updatedAt": ScheduleModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = ScheduleModel.id
    return fields


def get_subject_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": SubjectModel.id,
        "classId": SubjectModel.class_id,
        "name": SubjectModel.name,
        "createdAt": SubjectModel.created_at,
        "updatedAt": SubjectModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = SubjectModel.id
    return fields


def get_user_columns(field: list[str]) -> dict[str, object]:
    mapped_filed: dict[str, object] = {
        "id": UserModel.id,
        "username": UserModel.username,
        "email": UserModel.email,
        "password": UserModel.password,
        "avatarUrl": UserModel.avatar_url,
        "classId": UserModel.class_id,
        "createdAt": UserModel.created_at,
        "updatedAt": UserModel.updated_at,
    }
    fields = {f: mapped_filed[f] for f in field if f in mapped_filed}
    if "id" not in fields:
        fields["id"] = UserModel.id
    return fields
