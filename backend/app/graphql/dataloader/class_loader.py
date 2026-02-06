from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.get_column import (
    get_announcement_columns,
    get_assignment_columns,
    get_schedule_columns,
    get_subject_columns,
    get_user_columns,
)
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_model import AssignmentModel
from app.models.schedule_model import ScheduleModel
from app.models.subject_model import SubjectModel
from app.models.user_model import UserModel
from strawberry.dataloader import DataLoader


class ClassLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[UserModel]]
        ] = DataLoader(load_fn=self._load_users)
        self.subject_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[SubjectModel]]
        ] = DataLoader(load_fn=self._load_subjects)
        self.assignment_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AssignmentModel]]
        ] = DataLoader(load_fn=self._load_assignments)
        self.schedule_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[ScheduleModel]]
        ] = DataLoader(load_fn=self._load_schedules)
        self.announcement_loader: DataLoader[
            tuple[int, tuple[str, ...]], Optional[List[AnnouncementModel]]
        ] = DataLoader(load_fn=self._load_announcements)

    async def _load_users(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[UserModel]]]:
        try:
            fields = keys[0][1]
            class_ids = [key[0] for key in keys]
            column_dict = get_user_columns(list(fields))
            if "class_id" not in column_dict:
                column_dict["class_id"] = UserModel.class_id
            stmt = select(*column_dict.values()).where(UserModel.class_id.in_(class_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            user_map: dict[int, List[UserModel]] = {
                class_id: [] for class_id in class_ids
            }
            for user in users:
                if user["class_id"] is not None:
                    user_map[user["class_id"]].append(UserModel(**user))
            return [user_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            raise e

    async def _load_subjects(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[SubjectModel]]]:
        try:
            fields = keys[0][1]
            class_ids = [key[0] for key in keys]
            column_dict = get_subject_columns(list(fields))
            if "class_id" not in column_dict:
                column_dict["class_id"] = SubjectModel.class_id
            stmt = select(*column_dict.values()).where(SubjectModel.class_id.in_(class_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            subjects = result.mappings().all()
            subject_map: dict[int, List[SubjectModel]] = {
                class_id: [] for class_id in class_ids
            }
            for subject in subjects:
                if subject["class_id"] is not None:
                    subject_map[subject["class_id"]].append(SubjectModel(**subject))
            return [subject_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            raise e

    async def _load_assignments(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            fields = keys[0][1]
            class_ids = [key[0] for key in keys]
            column_dict = get_assignment_columns(list(fields))
            if "class_id" not in column_dict:
                column_dict["class_id"] = AssignmentModel.class_id
            stmt = select(*column_dict.values()).where(AssignmentModel.class_id.in_(class_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            assignments = result.mappings().all()
            assignment_map: dict[int, List[AssignmentModel]] = {
                class_id: [] for class_id in class_ids
            }
            for assignment in assignments:
                if assignment["class_id"] is not None:
                    assignment_map[assignment["class_id"]].append(
                        AssignmentModel(**assignment)
                    )
            return [assignment_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            raise e

    async def _load_schedules(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[ScheduleModel]]]:
        try:
            fields = keys[0][1]
            class_ids = [key[0] for key in keys]
            column_dict = get_schedule_columns(list(fields))
            if "class_id" not in column_dict:
                column_dict["class_id"] = ScheduleModel.class_id
            stmt = select(*column_dict.values()).where(ScheduleModel.class_id.in_(class_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            schedules = result.mappings().all()
            schedule_map: dict[int, List[ScheduleModel]] = {
                class_id: [] for class_id in class_ids
            }
            for subject in schedules:
                if subject["class_id"] is not None:
                    schedule_map[subject["class_id"]].append(ScheduleModel(**subject))
            return [schedule_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            raise e

    async def _load_announcements(
        self, keys: List[Tuple[int, Tuple[str, ...]]]
    ) -> List[Optional[List[AnnouncementModel]]]:
        try:
            fields = keys[0][1]
            class_ids = [key[0] for key in keys]
            column_dict = get_announcement_columns(list(fields))
            if "class_id" not in column_dict:
                column_dict["class_id"] = AnnouncementModel.class_id
            stmt = select(*column_dict.values()).where(AnnouncementModel.class_id.in_(class_ids))  # type: ignore
            result = await self.db.execute(stmt)  # type: ignore
            announcements = result.mappings().all()
            announcement_map: dict[int, List[AnnouncementModel]] = {
                class_id: [] for class_id in class_ids
            }
            for subject in announcements:
                if subject["class_id"] is not None:
                    announcement_map[subject["class_id"]].append(
                        AnnouncementModel(**subject)
                    )
            return [announcement_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            raise e
