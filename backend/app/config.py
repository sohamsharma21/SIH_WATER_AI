"""Configuration settings for the SIH WATER AI backend."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # MQTT Configuration
    MQTT_BROKER_URL: str = os.getenv("MQTT_BROKER_URL", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_USERNAME: Optional[str] = os.getenv("MQTT_USERNAME", None)
    MQTT_PASSWORD: Optional[str] = os.getenv("MQTT_PASSWORD", None)
    
    # Application Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SIH WATER AI"
    ENV: str = os.getenv("ENV", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Model Storage
    MODEL_DIR: str = os.path.join(os.path.dirname(__file__), "models")
    DATA_DIR: str = os.path.join(os.path.dirname(__file__), "..", "data")
    
    # Report Storage
    REPORTS_BUCKET: str = "reports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Validate required settings
if not settings.SUPABASE_URL:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("SUPABASE_URL not configured - some features will be unavailable")

if not settings.SUPABASE_KEY:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("SUPABASE_KEY not configured - some features will be unavailable")

# Ensure directories exist
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.DATA_DIR, exist_ok=True)

