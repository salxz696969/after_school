from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis

from .database import get_db
from .redis import redis
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

security = HTTPBearer()


class Context(BaseContext):
    def __init__(self, db: AsyncSession, redis: Redis):
        super().__init__()
        self.db = db
        self.redis = redis


async def get_context() -> AsyncGenerator[Context, None]:
    async for db in get_db():
        yield Context(db=db, redis=redis)
