from __future__ import annotations
from typing import List
import strawberry
from sqlalchemy.future import select
from app.core.context import Context
from app.graphql.types.user_type import UserType
from app.utils import extract_fields
from app.utils.get_column import get_user_columns


@strawberry.type
class UserQuery:
    @strawberry.field
    async def get_users(self, info: strawberry.Info[Context]) -> List[UserType]:
        try:
            fields = extract_fields(info)
            column_dict = get_user_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values())  # type: ignore
            result = await db.execute(stmt)  # type: ignore
            users = result.mappings().all()
            return [UserType(**user) for user in users]  # type: ignore
        except Exception as e:
            raise e
