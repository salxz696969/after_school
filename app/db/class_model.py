from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_model import UserModel
    from .subject_model import SubjectModel
    from .assignment_model import AssignmentModel
    from .schedule_model import ScheduleModel
    from .announcement_model import AnnouncementModel


class ClassModel(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    speciality: Mapped[str] = mapped_column(String, index=True)
    major: Mapped[str] = mapped_column(String, index=True)
    group_name: Mapped[str] = mapped_column(String, index=True)
    generation: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel", back_populates="class_"
    )
    subjects: Mapped[list["SubjectModel"]] = relationship(
        "SubjectModel", back_populates="class_"
    )
    assignments: Mapped[list["AssignmentModel"]] = relationship(
        "AssignmentModel", back_populates="class_"
    )
    schedules: Mapped[list["ScheduleModel"]] = relationship(
        "ScheduleModel", back_populates="class_"
    )
    announcements: Mapped[list["AnnouncementModel"]] = relationship(
        "AnnouncementModel", back_populates="class_"
    )
