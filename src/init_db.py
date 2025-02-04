from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config

url = f"mysql+aiomysql://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

_engine = create_async_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=900,
)
_engine_for_func = create_async_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=900,
)
_sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
_sessionmaker_for_func = async_sessionmaker(_engine_for_func, expire_on_commit=False)
