from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MADDS Placement Swarm"
    env: str = "development"
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    max_text_length: int = 30000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
