import os

DATABASE = os.getenv(
    "DATABASE", "postgresql+asyncpg://postgres:postgres@localhost:5432/Workmate"
)
SYNC_DATABASE = os.getenv(
    "SYNC_DATABASE", "postgresql://postgres:postgres@localhost:5432/Workmate"
)
