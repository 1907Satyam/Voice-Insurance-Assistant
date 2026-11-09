import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)


@dataclass(frozen=True)
class Settings:
    project_name: str
    database_url: str
    gnani_api_key_id: str
    prisma_stt_url: str
    evon_llm_url: str
    timbre_tts_url: str
    evon_model: str
    timbre_voice: str
    timbre_model: str
    cors_origins: list[str]
    max_audio_size_mb: int
    max_document_size_mb: int
    upload_dir: str

    @classmethod
    def from_environment(cls) -> "Settings":
        project_name = os.getenv("PROJECT_NAME", "").strip()
        database_url = os.getenv("DATABASE_URL", "").strip()
        upload_dir = os.getenv("UPLOAD_DIR", "").strip()
        if not project_name:
            raise ValueError("PROJECT_NAME must be set in backend/.env.")
        if not database_url:
            raise ValueError("DATABASE_URL must be set in backend/.env.")
        if not upload_dir:
            raise ValueError("UPLOAD_DIR must be set in backend/.env.")

        return cls(
            project_name=project_name,
            database_url=database_url,
            gnani_api_key_id=os.getenv("GNANI_API_KEY_ID", "").strip(),
            prisma_stt_url=os.getenv("PRISMA_STT_URL", "").strip(),
            evon_llm_url=os.getenv("EVON_LLM_URL", "").strip(),
            timbre_tts_url=os.getenv("TIMBRE_TTS_URL", "").strip(),
            evon_model=os.getenv("EVON_MODEL", "").strip(),
            timbre_voice=os.getenv("TIMBRE_VOICE", "Nalini").strip(),
            timbre_model=os.getenv("TIMBRE_MODEL", "timbre-v2.5").strip(),
            cors_origins=[
                origin.strip()
                for origin in os.getenv(
                    "CORS_ORIGINS",
                    "http://localhost:5173,https://voice-insurance-assistant.vercel.app",
                ).split(",")
                if origin.strip()
            ],
            max_audio_size_mb=int(os.getenv("MAX_AUDIO_SIZE_MB", "15")),
            max_document_size_mb=int(os.getenv("MAX_DOCUMENT_SIZE_MB", "10")),
            upload_dir=upload_dir,
        )


settings = Settings.from_environment()


def sqlalchemy_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url
