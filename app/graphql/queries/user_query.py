from __future__ import annotations
import logging
from typing import List
from fastapi import HTTPException
import strawberry
from sqlalchemy.future import select
from app.core.context import Context
from app.graphql.types.user_type import UserType
from app.utils import extract_fields, validate_fields
from app.utils.get_column import ColumnGetter


@strawberry.type
class UserQuery:
    @strawberry.field
    async def get_users(self, info: strawberry.Info[Context]) -> List[UserType]:
        try:
            if not validate_fields(info, "user"):
                raise HTTPException(
                    status_code=400,
                    detail="Recursive in user detected. Please remove it from your query.",
                )
            fields = extract_fields(info)
            column_list = ColumnGetter.get_user_columns(fields)
            async with info.context.sessionmaker() as session:  # type: ignore
                stmt = select(*column_list)  # type: ignore
                result = await session.execute(stmt)  # type: ignore
                users = result.mappings().all()  # type: ignore
                return [UserType(**user) for user in users]  # type: ignore
        except Exception as e:
            logging.exception(f"Error fetching users: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch users")
