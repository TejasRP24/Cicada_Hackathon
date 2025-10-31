import os
from dotenv import load_dotenv

# ✅ Dynamically find .env file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

# If .env isn't in the same folder, try the parent one
if not os.path.exists(env_path):
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")

load_dotenv(dotenv_path=env_path)

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "mental_wellness")

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    PROJECT_NAME: str = "Mental Wellness Mirror"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

settings = Settings()

# ✅ Debug check — print first 5 chars only (safe)
print("DEBUG: GOOGLE_API_KEY =", settings.GOOGLE_API_KEY[:5] + "..." if settings.GOOGLE_API_KEY else "NOT FOUND")
