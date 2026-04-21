import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # -----------------------------
    # App Config
    # -----------------------------
    APP_NAME: str = "AI Resume Recommender"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # -----------------------------
    # Database Config
    # -----------------------------
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME: str = os.getenv("DB_NAME", "resume_db")

    # -----------------------------
    # LLM Provider Config
    # -----------------------------
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai | local

    # -----------------------------
    # OpenAI Config
    # -----------------------------
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    # -----------------------------
    # Local Model (Ollama) Config
    # -----------------------------
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

    # -----------------------------
    # Embedding Model
    # -----------------------------
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # -----------------------------
    # Vector Search Config
    # -----------------------------
    VECTOR_INDEX: str = os.getenv("VECTOR_INDEX", "resume_index")
    VECTOR_LIMIT: int = int(os.getenv("VECTOR_LIMIT", 5))
    VECTOR_CANDIDATES: int = int(os.getenv("VECTOR_CANDIDATES", 100))

    # -----------------------------
    # Validation
    # -----------------------------
    def validate(self):
        if self.LLM_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY is required when using OpenAI")

        if self.LLM_PROVIDER not in ["openai", "local"]:
            raise ValueError("❌ LLM_PROVIDER must be 'openai' or 'local'")


# Singleton settings instance
settings = Settings()

# Run validation on import
settings.validate()