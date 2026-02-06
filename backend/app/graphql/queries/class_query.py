from __future__ import annotations
from sqlalchemy import select
import strawberry
from app.core.context import Context
from app.utils.get_column import get_class_columns
from app.graphql.types.class_type import ClassType
from app.utils import extract_fields


@strawberry.type
class ClassQuery:
    @strawberry.field
    async def get_classes(self, info: strawberry.Info[Context]) -> list[ClassType]:
        try:
            fields = extract_fields(info)
            column_dict = get_class_columns(fields)
            db = info.context.db
            stmt = select(*column_dict.values()) # type: ignore
            result = await db.execute(stmt) # type: ignore
            classes = result.mappings().all()
            return [ClassType(**cls) for cls in classes] # type: ignore
        except Exception as e:
            raise e
