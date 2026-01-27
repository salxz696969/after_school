from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.announcement_model import AnnouncementModel
from app.models.assignment_model import AssignmentModel
from app.models.schedule_model import ScheduleModel
from app.models.subject_model import SubjectModel
from app.models.user_model import UserModel
from strawberry.dataloader import DataLoader


class ClassLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_loader: DataLoader[int, Optional[List[UserModel]]] = DataLoader(
            load_fn=lambda ids: self._load_users(ids, db)
        )
        self.subject_loader: DataLoader[int, Optional[List[SubjectModel]]] = DataLoader(
            load_fn=lambda ids: self._load_subjects(ids, db)
        )
        self.assignment_loader: DataLoader[int, Optional[List[AssignmentModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_assignments(ids, db))
        )
        self.schedule_loader: DataLoader[int, Optional[List[ScheduleModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_schedules(ids, db))
        )
        self.announcement_loader: DataLoader[int, Optional[List[AnnouncementModel]]] = (
            DataLoader(load_fn=lambda ids: self._load_announcements(ids, db))
        )

    async def _load_users(
        self, class_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[UserModel]]]:
        stmt = select(UserModel).where(UserModel.class_id.in_(class_ids))
        result = await db.execute(stmt)
        users = result.scalars().all()
        user_map: dict[int, List[UserModel]] = {class_id: [] for class_id in class_ids}
        for user in users:
            if user.class_id is not None:
                user_map[user.class_id].append(user)
        return [user_map.get(class_id, []) for class_id in class_ids]

    async def _load_subjects(
        self, class_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[SubjectModel]]]:
        stmt = select(SubjectModel).where(SubjectModel.class_id.in_(class_ids))
        result = await db.execute(stmt)
        subjects = result.scalars().all()
        subject_map: dict[int, List[SubjectModel]] = {
            class_id: [] for class_id in class_ids
        }
        for subject in subjects:
            if subject.class_id is not None:
                subject_map[subject.class_id].append(subject)
        return [subject_map.get(class_id, []) for class_id in class_ids]

    async def _load_assignments(
        self, class_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AssignmentModel]]]:
        stmt = select(AssignmentModel).where(AssignmentModel.class_id.in_(class_ids))
        result = await db.execute(stmt)
        assignments = result.scalars().all()
        assignment_map: dict[int, List[AssignmentModel]] = {
            class_id: [] for class_id in class_ids
        }
        for assignment in assignments:
            if assignment.class_id is not None:
                assignment_map[assignment.class_id].append(assignment)
        return [assignment_map.get(class_id, []) for class_id in class_ids]

    async def _load_schedules(
        self, class_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[ScheduleModel]]]:
        stmt = select(ScheduleModel).where(ScheduleModel.class_id.in_(class_ids))
        result = await db.execute(stmt)
        schedules = result.scalars().all()
        schedule_map: dict[int, List[ScheduleModel]] = {
            class_id: [] for class_id in class_ids
        }
        for schedule in schedules:
            if schedule.class_id is not None:
                schedule_map[schedule.class_id].append(schedule)
        return [schedule_map.get(class_id, []) for class_id in class_ids]

    async def _load_announcements(
        self, class_ids: List[int], db: AsyncSession
    ) -> List[Optional[List[AnnouncementModel]]]:
        stmt = select(AnnouncementModel).where(
            AnnouncementModel.class_id.in_(class_ids)
        )
        result = await db.execute(stmt)
        announcements = result.scalars().all()
        announcement_map: dict[int, List[AnnouncementModel]] = {
            class_id: [] for class_id in class_ids
        }
        for announcement in announcements:
            if announcement.class_id is not None:
                announcement_map[announcement.class_id].append(announcement)
        return [announcement_map.get(class_id, []) for class_id in class_ids]
