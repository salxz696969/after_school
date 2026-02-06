from __future__ import annotations
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields
from app.utils.get_column import get_subject_columns
from app.core.context import Context
from app.graphql.types.subject_type import SubjectType

@strawberry.type
class SubjectQuery:
    @strawberry.field
    async def get_subjects(self, info: strawberry.Info[Context]) -> List[SubjectType]:
        try:
            fields = extract_fields(info)
            column_dict = get_subject_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            subjects = result.mappings().all()
            return [SubjectType(**subject) for subject in subjects]  # type: ignore
        except Exception as e:
            raise e