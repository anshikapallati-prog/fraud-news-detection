"""
TruthLens AI — Configuration Module
Loads environment variables and provides application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Signs auth session tokens. Must be long and random; never share it.
    # Generate one with: python -c "import secrets; print(secrets.token_urlsafe(48))"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # Input constraints
    MAX_INPUT_LENGTH: int = int(os.getenv("MAX_INPUT_LENGTH", "15000"))
    MIN_INPUT_LENGTH: int = int(os.getenv("MIN_INPUT_LENGTH", "20"))

    # API settings
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "60"))

    # CORS — allowed origins (comma-separated)
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")

    def validate(self) -> None:
        """Validate that critical settings are present."""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Please add it to backend/.env (see .env.example)."
            )
        if not self.GROQ_MODEL:
            raise ValueError(
                "GROQ_MODEL is not set. "
                "Please specify a valid Groq model name in backend/.env."
            )


settings = Settings()
