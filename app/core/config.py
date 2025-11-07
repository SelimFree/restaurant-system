from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Loads and validates application settings from environment variables.
    """
    
    # --- Database Config ---
    #
    DATABASE_URL: str
    
    # --- Redis Config ---
    #
    REDIS_HOST: str
    REDIS_PORT: int
    
    # --- API/JWT Config ---
    #
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Load settings from the .env file
    #
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()