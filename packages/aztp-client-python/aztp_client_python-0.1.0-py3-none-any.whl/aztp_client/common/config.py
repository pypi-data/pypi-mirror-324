import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class ClientConfig(BaseModel):
    api_key: str
    base_url: str = Field(default="https://api.aztp.ai")
    environment: str = Field(default="production")
    timeout: int = Field(default=30)

    @classmethod
    def from_env(cls) -> "ClientConfig":
        """Create configuration from environment variables."""
        return cls(
            api_key=os.getenv("AZTP_API_KEY", ""),
            base_url=os.getenv("AZTP_BASE_URL", "https://api.aztp.ai"),
            environment=os.getenv("AZTP_ENVIRONMENT", "production"),
            timeout=int(os.getenv("AZTP_TIMEOUT", "30")),
        )

    @classmethod
    def create(
        cls,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        environment: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> "ClientConfig":
        """Create configuration with optional overrides."""
        config = cls.from_env()
        
        if api_key:
            config.api_key = api_key
        if base_url:
            config.base_url = base_url
        if environment:
            config.environment = environment
        if timeout:
            config.timeout = timeout
            
        return config 