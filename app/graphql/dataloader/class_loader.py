import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from app.utils.get_column import ColumnGetter
from app.core.database import AsyncSessionLocal
from app.db.announcement_model import AnnouncementModel
from app.db.assignment_model import AssignmentModel
from app.db.schedule_model import ScheduleModel
from app.db.subject_model import SubjectModel
from app.db.user_model import UserModel
from strawberry.dataloader import DataLoader


class ClassLoader:
    def __init__(self, sessionmaker: AsyncSessionLocal):  # type: ignore
        self.sessionmaker = sessionmaker  # type: ignore
        self._user_fields: List[str] | None = None
        self._subject_fields: List[str] | None = None
        self._assignment_fields: List[str] | None = None
        self._schedule_fields: List[str] | None = None
        self._announcement_fields: List[str] | None = None
        self.user_loader: DataLoader[int, Optional[List[UserModel]]] | None = None
        self.subject_loader: DataLoader[int, Optional[List[SubjectModel]]] | None = None
        self.assignment_loader: (
            DataLoader[int, Optional[List[AssignmentModel]]] | None
        ) = None
        self.schedule_loader: DataLoader[int, Optional[List[ScheduleModel]]] | None = (
            None
        )
        self.announcement_loader: (
            DataLoader[int, Optional[List[AnnouncementModel]]] | None
        ) = None

    def create_user_loader(self, fields: List[str]) -> None:
        self._user_fields = fields
        self.user_loader = DataLoader(load_fn=self._load_users)

    def create_subject_loader(self, fields: List[str]) -> None:
        self._subject_fields = fields
        self.subject_loader = DataLoader(load_fn=self._load_subjects)

    def create_assignment_loader(self, fields: List[str]) -> None:
        self._assignment_fields = fields
        self.assignment_loader = DataLoader(load_fn=self._load_assignments)

    def create_schedule_loader(self, fields: List[str]) -> None:
        self._schedule_fields = fields
        self.schedule_loader = DataLoader(load_fn=self._load_schedules)

    def create_announcement_loader(self, fields: List[str]) -> None:
        self._announcement_fields = fields
        self.announcement_loader = DataLoader(load_fn=self._load_announcements)

    async def _load_users(self, keys: List[int]) -> List[Optional[List[UserModel]]]:
        try:
            if not self._user_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            class_ids = keys
            column_list = ColumnGetter.get_user_columns(list(self._user_fields))
            if "classId" not in self._user_fields:
                column_list.append(UserModel.class_id)
            stmt = select(*column_list).where(UserModel.class_id.in_(class_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                user_map: dict[int, List[UserModel]] = {
                    class_id: [] for class_id in class_ids
                }
                for user in users:  # type: ignore
                    if user["class_id"] is not None:
                        user_map[user["class_id"]].append(UserModel(**user))
                return [user_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            logging.exception(f"Error loading users: {e}")
            raise HTTPException(status_code=500, detail="Failed to load users")

    async def _load_subjects(
        self, keys: List[int]
    ) -> List[Optional[List[SubjectModel]]]:
        try:
            if not self._subject_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            class_ids = keys
            column_list = ColumnGetter.get_subject_columns(list(self._subject_fields))
            if "classId" not in self._subject_fields:
                column_list.append(SubjectModel.class_id)
            stmt = select(*column_list).where(SubjectModel.class_id.in_(class_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                subjects = result.mappings().all()  # type: ignore
                subject_map: dict[int, List[SubjectModel]] = {
                    class_id: [] for class_id in class_ids
                }
            for subject in subjects:  # type: ignore
                if subject["class_id"] is not None:
                    subject_map[subject["class_id"]].append(SubjectModel(**subject))
            return [subject_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            logging.exception(f"Error loading subjects: {e}")
            raise HTTPException(status_code=500, detail="Failed to load subjects")

    async def _load_assignments(
        self, keys: List[int]
    ) -> List[Optional[List[AssignmentModel]]]:
        try:
            if not self._assignment_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            class_ids = keys
            column_list = ColumnGetter.get_assignment_columns(list(self._assignment_fields))
            if "classId" not in self._assignment_fields:
                column_list.append(AssignmentModel.class_id)
            stmt = select(*column_list).where(AssignmentModel.class_id.in_(class_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                assignments = result.mappings().all()  # type: ignore
                assignment_map: dict[int, List[AssignmentModel]] = {
                    class_id: [] for class_id in class_ids
                }
            for assignment in assignments:  # type: ignore
                if assignment["class_id"] is not None:
                    assignment_map[assignment["class_id"]].append(
                        AssignmentModel(**assignment)
                    )
            return [assignment_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            logging.exception(f"Error loading assignments: {e}")
            raise HTTPException(status_code=500, detail="Failed to load assignments")

    async def _load_schedules(
        self, keys: List[int]
    ) -> List[Optional[List[ScheduleModel]]]:
        try:
            if not self._schedule_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            class_ids = keys
            column_list = ColumnGetter.get_schedule_columns(list(self._schedule_fields))
            if "classId" not in self._schedule_fields:
                column_list.append(ScheduleModel.class_id)
            stmt = select(*column_list).where(ScheduleModel.class_id.in_(class_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                schedules = result.mappings().all()  # type: ignore
                schedule_map: dict[int, List[ScheduleModel]] = {
                    class_id: [] for class_id in class_ids
                }
            for subject in schedules:  # type: ignore
                if subject["class_id"] is not None:
                    schedule_map[subject["class_id"]].append(ScheduleModel(**subject))
            return [schedule_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            logging.exception(f"Error loading schedules: {e}")
            raise HTTPException(status_code=500, detail="Failed to load schedules")

    async def _load_announcements(
        self, keys: List[int]
    ) -> List[Optional[List[AnnouncementModel]]]:
        try:
            if not self._announcement_fields:
                raise HTTPException(status_code=500, detail="Fields not set")
            class_ids = keys
            column_list = ColumnGetter.get_announcement_columns(list(self._announcement_fields))
            if "classId" not in self._announcement_fields:
                column_list.append(AnnouncementModel.class_id)
            stmt = select(*column_list).where(AnnouncementModel.class_id.in_(class_ids))  # type: ignore
            async with self.sessionmaker() as session:  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                announcements = result.mappings().all()  # type: ignore
                announcement_map: dict[int, List[AnnouncementModel]] = {
                    class_id: [] for class_id in class_ids
                }
            for subject in announcements:  # type: ignore
                if subject["class_id"] is not None:
                    announcement_map[subject["class_id"]].append(
                        AnnouncementModel(**subject)
                    )
            return [announcement_map.get(class_id, []) for class_id in class_ids]
        except Exception as e:
            logging.exception(f"Error loading announcements: {e}")
            raise HTTPException(status_code=500, detail="Failed to load announcements")
