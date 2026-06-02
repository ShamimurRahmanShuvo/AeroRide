import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings:
    DATABSE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


settings = Settings()
