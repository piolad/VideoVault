import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "database_url": os.getenv("DATABASE_URL", "postgresql://postgres:root@localhost:5432/videos")
}