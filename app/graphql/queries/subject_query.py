from __future__ import annotations
from fastapi import HTTPException
import strawberry
from typing import List
from sqlalchemy.future import select
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter
from app.core.context import Context
from app.graphql.types.subject_type import SubjectType
import logging

@strawberry.type
class SubjectQuery:
    @strawberry.field
    async def get_subjects(self, info: strawberry.Info[Context]) -> List[SubjectType]:
        try:
            if not validate_fields(info, "subject"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in subject detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_subject_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                subjects = result.mappings().all()  # type: ignore
                return [SubjectType(**subject) for subject in subjects]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching subjects: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch subjects")
