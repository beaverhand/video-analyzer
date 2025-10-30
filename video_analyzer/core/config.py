import os
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Analyzer"
    VERSION: str = "1.0.0"
    API_STR: str = ""
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # File Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    STATIC_DIR: Path = BASE_DIR / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"

    # OpenRouter Settings
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

settings = Settings()
