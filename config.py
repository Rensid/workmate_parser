import os

SYNC_DATABASE = os.getenv(
    "SYNC_DATABASE", "postgresql://postgres:Lihobor0754133@localhost:5432/postgres"
)
