import redis.asyncio as rs
from config import config


redis = rs.Redis(
    host=config.db_redis.host,
    port=config.db_redis.port,
    db=config.db_redis.db,
)
