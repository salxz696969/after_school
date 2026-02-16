from typing import List
from app.db.class_model import ClassModel
from app.db.announcement_content_model import AnnouncementContentModel
from app.db.announcement_model import AnnouncementModel
from app.db.assignment_content_model import AssignmentContentModel
from app.db.assignment_model import AssignmentModel
from app.db.assignment_reply_content_model import AssignmentReplyContentModel
from app.db.assignment_reply_model import AssignmentReplyModel
from app.db.chat_content_model import ChatContentModel
from app.db.chat_model import ChatModel
from app.db.chat_room_member_model import ChatRoomMemberModel
from app.db.chat_room_model import ChatRoomModel
from app.db.media_model import MediaModel
from app.db.schedule_content_model import ScheduleContentModel
from app.db.schedule_model import ScheduleModel
from app.db.subject_model import SubjectModel
from app.db.user_model import UserModel


class ColumnGetter:
    @staticmethod
    def _build_fields(
        field: list[str],
        mapped_field: dict[str, object],
    ) -> List[object]:
        fields = [mapped_field[f] for f in field if f in mapped_field]
        if "id" not in field:
            fields.append(mapped_field["id"])
        return fields

    @staticmethod
    def get_class_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ClassModel.id,
            "speciality": ClassModel.speciality,
            "major": ClassModel.major,
            "groupName": ClassModel.group_name,
            "generation": ClassModel.generation,
            "createdAt": ClassModel.created_at,
            "updatedAt": ClassModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_announcement_content_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AnnouncementContentModel.id,
            "text": AnnouncementContentModel.text,
            "announcementId": AnnouncementContentModel.announcement_id,
            "createdAt": AnnouncementContentModel.created_at,
            "updatedAt": AnnouncementContentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_announcement_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AnnouncementModel.id,
            "userId": AnnouncementModel.user_id,
            "classId": AnnouncementModel.class_id,
            "type": AnnouncementModel.type,
            "createdAt": AnnouncementModel.created_at,
            "updatedAt": AnnouncementModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_assignment_content_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AssignmentContentModel.id,
            "text": AssignmentContentModel.text,
            "assignmentId": AssignmentContentModel.assignment_id,
            "createdAt": AssignmentContentModel.created_at,
            "updatedAt": AssignmentContentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_assignment_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AssignmentModel.id,
            "userId": AssignmentModel.user_id,
            "subjectId": AssignmentModel.subject_id,
            "classId": AssignmentModel.class_id,
            "createdAt": AssignmentModel.created_at,
            "updatedAt": AssignmentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_assignment_reply_content_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AssignmentReplyContentModel.id,
            "text": AssignmentReplyContentModel.text,
            "assignmentReplyId": AssignmentReplyContentModel.assignment_reply_id,
            "createdAt": AssignmentReplyContentModel.created_at,
            "updatedAt": AssignmentReplyContentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_assignment_reply_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": AssignmentReplyModel.id,
            "assignmentId": AssignmentReplyModel.assignment_id,
            "userId": AssignmentReplyModel.user_id,
            "upVote": AssignmentReplyModel.up_vote,
            "downVote": AssignmentReplyModel.down_vote,
            "createdAt": AssignmentReplyModel.created_at,
            "updatedAt": AssignmentReplyModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_chat_content_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ChatContentModel.id,
            "text": ChatContentModel.text,
            "chatId": ChatContentModel.chat_id,
            "createdAt": ChatContentModel.created_at,
            "updatedAt": ChatContentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_chat_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ChatModel.id,
            "chatRoomId": ChatModel.chat_room_id,
            "userId": ChatModel.user_id,
            "createdAt": ChatModel.created_at,
            "updatedAt": ChatModel.updated_at,
        }
        extracted_fields = ColumnGetter._build_fields(field, mapped_field)
        if "chatRoomId" not in field and "chatRoom" in field:
            extracted_fields.append(ChatModel.chat_room_id)
        if "userId" not in field and "user" in field:
            extracted_fields.append(ChatModel.user_id)
        return extracted_fields

    @staticmethod
    def get_chat_room_member_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ChatRoomMemberModel.id,
            "chatRoomId": ChatRoomMemberModel.chat_room_id,
            "userId": ChatRoomMemberModel.user_id,
            "createdAt": ChatRoomMemberModel.created_at,
            "updatedAt": ChatRoomMemberModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_chat_room_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ChatRoomModel.id,
            "chat_room_type": ChatRoomModel.chat_room_type,
            "chatRoomName": ChatRoomModel.chat_room_name,
            "avatarUrl": ChatRoomModel.avatar_url,
            "createdAt": ChatRoomModel.created_at,
            "updatedAt": ChatRoomModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_media_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
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
        extracted_fields = ColumnGetter._build_fields(field, mapped_field)
        if "chatContentId" not in field and "chatContent" in field:
            extracted_fields.append(MediaModel.chat_content_id)
        if "scheduleContentId" not in field and "scheduleContent" in field:
            extracted_fields.append(MediaModel.schedule_content_id)
        if "announcementContentId" not in field and "announcementContent" in field:
            extracted_fields.append(MediaModel.announcement_content_id)
        if "assignmentContentId" not in field and "assignmentContent" in field:
            extracted_fields.append(MediaModel.assignment_content_id)
        if (
            "assignmentReplyContentId" not in field
            and "assignmentReplyContent" in field
        ):
            extracted_fields.append(MediaModel.assignment_reply_content_id)
        return extracted_fields

    @staticmethod
    def get_schedule_content_columns(
        field: list[str],
    ) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ScheduleContentModel.id,
            "text": ScheduleContentModel.text,
            "scheduleId": ScheduleContentModel.schedule_id,
            "createdAt": ScheduleContentModel.created_at,
            "updatedAt": ScheduleContentModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_schedule_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": ScheduleModel.id,
            "classId": ScheduleModel.class_id,
            "createdAt": ScheduleModel.created_at,
            "updatedAt": ScheduleModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_subject_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": SubjectModel.id,
            "classId": SubjectModel.class_id,
            "name": SubjectModel.name,
            "createdAt": SubjectModel.created_at,
            "updatedAt": SubjectModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)

    @staticmethod
    def get_user_columns(field: list[str]) -> List[object]:
        mapped_field: dict[str, object] = {
            "id": UserModel.id,
            "classId": UserModel.class_id,
            "username": UserModel.username,
            "email": UserModel.email,
            "password": UserModel.password,
            "avatarUrl": UserModel.avatar_url,
            "createdAt": UserModel.created_at,
            "updatedAt": UserModel.updated_at,
        }
        return ColumnGetter._build_fields(field, mapped_field)
