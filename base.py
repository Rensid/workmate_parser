from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import SYNC_DATABASE

engine = create_engine(SYNC_DATABASE, pool_pre_ping=True)

session_maker = sessionmaker(engine, expire_on_commit=False)


def get_session():
    with session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


def init_models():
    Base.metadata.create_all(bind=engine)


def run_migrations() -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", SYNC_DATABASE)
    command.upgrade(alembic_cfg, "head")
