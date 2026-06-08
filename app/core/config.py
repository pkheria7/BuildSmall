from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "KnowledgeHub"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "knowledge_base"

    NEMOTRON_PARSE_MODEL: str = "Qwen/Qwen2-VL-2B-Instruct"
    NEMOTRON_EMBED_MODEL: str = "nvidia/llama-nemotron-colembed-vl-3b-v2"
    EMBEDDING_DEVICE: str = "cpu"
    HF_TOKEN: str = ""
    NVIDIA_API_KEY: str = ""
    NVIDIA_CHAT_MODEL: str = "nvidia/nvidia-nemotron-nano-9b-v2"
    NVIDIA_API_URL: str = "https://integrate.api.nvidia.com/v1"

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    CHUNK_SIZE: int = 1100
    CHUNK_OVERLAP: int = 180
    ZEROGPU_DURATION_SECONDS: int = 180
    CHAT_TEMPERATURE: float = 0.6
    CHAT_TOP_P: float = 0.95
    CHAT_MAX_TOKENS: int = 2048
    MIN_THINKING_TOKENS: int = 1024
    MAX_THINKING_TOKENS: int = 2048

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_qdrant_url(self) -> str:
        if self.QDRANT_URL.startswith("https://") and ":" not in self.QDRANT_URL[8:]:
            return f"{self.QDRANT_URL}:443"
        return self.QDRANT_URL


settings = Settings()
