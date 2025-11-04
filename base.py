from alembic import command
from alembic.config import Config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import SYNC_DATABASE, DATABASE
from contextlib import asynccontextmanager

engine = create_async_engine(
    DATABASE,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_async_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


class Base(DeclarativeBase):
    pass


def init_models():
    Base.metadata.create_all(bind=engine)


def run_migrations() -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", SYNC_DATABASE)
    command.upgrade(alembic_cfg, "head")
