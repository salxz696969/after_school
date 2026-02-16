from redis.asyncio import Redis
from app.core.config import setting

redis = Redis.from_url(
    setting.RADIS_URL,
    encoding="utf-8",
    decode_responses=True,
)
