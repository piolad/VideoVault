import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "database_url": os.getenv("DATABASE_URL", "postgresql://localhost:5432/default_db")
}