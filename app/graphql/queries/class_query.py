from __future__ import annotations
import logging
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select
import strawberry
from app.core.context import Context
from app.db.class_model import ClassModel
from app.utils.get_column import ColumnGetter
from app.graphql.types.class_type import ClassType
from app.utils import extract_fields, validate_fields


@strawberry.input
class WhereClause:
    group_name: str | None = None
    id: int | None = None


@strawberry.type
class ClassQuery:
    @strawberry.field
    async def get_class(
        self, info: strawberry.Info[Context], where: Optional[WhereClause]
    ) -> ClassType | None:
        try:
            if not validate_fields(info, "class_"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in class_ detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_class_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                if where and where.id is not None:
                    stmt = stmt.where(ClassModel.id == where.id)  # type: ignore
                if where and where.group_name is not None:
                    stmt = stmt.where(ClassModel.group_name == where.group_name)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                cls = result.mappings().first()  # type: ignore
                return ClassType(**cls) if cls else None  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching class with id {id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch class")

    @strawberry.field
    async def get_classes(self, info: strawberry.Info[Context]) -> list[ClassType]:
        try:
            if not validate_fields(info, "class_"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in class_ detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_class_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                classes = result.mappings().all()  # type: ignore
                return [ClassType(**cls) for cls in classes]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching classes: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch classes")
