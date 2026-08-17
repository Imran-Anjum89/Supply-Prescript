import os
from pathlib import Path

# Automatically load environment variables from backend/.env if it exists
backend_dir = Path(__file__).resolve().parent.parent
env_file = backend_dir / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))

class Settings:
    PROJECT_NAME: str = "SupplyPrescript"
    API_V1_STR: str = ""
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-supply-prescript-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./supplyprescript.db")

settings = Settings()
