import strawberry
from strawberry.extensions import QueryDepthLimiter
from app.graphql.queries import (
    AssignmentReplyQuery,
    ChatRoomMemberQuery,
    UserQuery,
    ScheduleQuery,
    SubjectQuery,
    ChatRoomQuery,
    ClassQuery,
    AnnouncementQuery,
    AssignmentQuery,
    ChatQuery,
    ScheduleContentQuery,
    AssignmentContentQuery,
    AnnouncementContentQuery,
    ChatContentQuery,
    AssignmentReplyContentQuery,
    MediaQuery,
)

from app.graphql.mutations import (
    UserMutation,
    SubjectMutation,
    ScheduleMutation,
    AssignmentMutation,
    AnnouncementMutation,
    ChatMutation,
    ChatRoomMutation,
    ChatRoomMemberMutation,
    AssignmentReplyMutation,
    MediaMutation,
    AssignmentReplyContentMutation,
    ChatContentMutation,
    ScheduleContentMutation,
    AnnouncementContentMutation,
    AssignmentContentMutation,
    ClassMutation,
)


@strawberry.type
class Query:
    @strawberry.field
    def announcement(self) -> AnnouncementQuery:
        return AnnouncementQuery()

    @strawberry.field
    def assignment(self) -> AssignmentQuery:
        return AssignmentQuery()

    @strawberry.field
    def assignment_reply(self) -> AssignmentReplyQuery:
        return AssignmentReplyQuery()

    @strawberry.field
    def chat(self) -> ChatQuery:
        return ChatQuery()

    @strawberry.field
    def chat_room(self) -> ChatRoomQuery:
        return ChatRoomQuery()

    @strawberry.field
    def chat_room_member(self) -> ChatRoomMemberQuery:
        return ChatRoomMemberQuery()

    @strawberry.field
    def class_(self) -> ClassQuery:
        return ClassQuery()

    @strawberry.field
    def schedule(self) -> ScheduleQuery:
        return ScheduleQuery()

    @strawberry.field
    def subject(self) -> SubjectQuery:
        return SubjectQuery()

    @strawberry.field
    def user(self) -> UserQuery:
        return UserQuery()

    @strawberry.field
    def schedule_content(self) -> ScheduleContentQuery:
        return ScheduleContentQuery()

    @strawberry.field
    def assignment_content(self) -> AssignmentContentQuery:
        return AssignmentContentQuery()

    @strawberry.field
    def announcement_content(self) -> AnnouncementContentQuery:
        return AnnouncementContentQuery()

    @strawberry.field
    def chat_content(self) -> ChatContentQuery:
        return ChatContentQuery()

    @strawberry.field
    def assignment_reply_content(self) -> AssignmentReplyContentQuery:
        return AssignmentReplyContentQuery()

    @strawberry.field
    def media(self) -> MediaQuery:
        return MediaQuery()


@strawberry.type
class Mutation:
    @strawberry.field
    def announcement_content_mutation(self) -> AnnouncementContentMutation:
        return AnnouncementContentMutation()

    @strawberry.field
    def assignment_content_mutation(self) -> AssignmentContentMutation:
        return AssignmentContentMutation()

    @strawberry.field
    def schedule_mutation(self) -> ScheduleMutation:
        return ScheduleMutation()

    @strawberry.field
    def subject_mutation(self) -> SubjectMutation:
        return SubjectMutation()

    @strawberry.field
    def user_mutation(self) -> UserMutation:
        return UserMutation()

    @strawberry.field
    def assignment_mutation(self) -> AssignmentMutation:
        return AssignmentMutation()

    @strawberry.field
    def announcement_mutation(self) -> AnnouncementMutation:
        return AnnouncementMutation()

    @strawberry.field
    def chat_mutation(self) -> ChatMutation:
        return ChatMutation()

    @strawberry.field
    def chat_room_mutation(self) -> ChatRoomMutation:
        return ChatRoomMutation()

    @strawberry.field
    def chat_room_member_mutation(self) -> ChatRoomMemberMutation:
        return ChatRoomMemberMutation()

    @strawberry.field
    def assignment_reply_mutation(self) -> AssignmentReplyMutation:
        return AssignmentReplyMutation()

    @strawberry.field
    def media_mutation(self) -> MediaMutation:
        return MediaMutation()

    @strawberry.field
    def assignment_reply_content_mutation(self) -> AssignmentReplyContentMutation:
        return AssignmentReplyContentMutation()

    @strawberry.field
    def chat_content_mutation(self) -> ChatContentMutation:
        return ChatContentMutation()

    @strawberry.field
    def schedule_content_mutation(self) -> ScheduleContentMutation:
        return ScheduleContentMutation()

    @strawberry.field
    def class_mutation(self) -> ClassMutation:
        return ClassMutation()


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[QueryDepthLimiter(max_depth=10)]
)
