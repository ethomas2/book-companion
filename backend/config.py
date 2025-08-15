import os
from typing import Optional

class Config:
    """Configuration class for the Book Companion API"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """Get OpenAI configuration as a dictionary"""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_MODEL
        }

# Global config instance
config = Config() 