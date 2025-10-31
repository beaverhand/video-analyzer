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

    # Model Settings
    MODEL: str = os.getenv("MODEL", "Qwen/Qwen3-VL-4B-Instruct")

    # VLLM Settings
    VLLM_PORT: str = os.getenv("VLLM_PORT", '22002')

    # OpenRouter Settings
    API_KEY: str = os.getenv("API_KEY", "")
    BASE_URL_TEMPLATE: str = os.getenv("BASE_URL", "https://localhost:{VLLM_PORT}/api/v1")
    BASE_URL: str | None = None

    def model_post_init(self, __context):
        self.BASE_URL = self.BASE_URL_TEMPLATE.format(VLLM_PORT=self.VLLM_PORT)


settings = Settings()
