"""Application configuration."""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from wombat_mcp.compat import promote_legacy_env

# Promote legacy WAFPASS_* settings before Settings() reads the environment.
promote_legacy_env()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    wombat_api_base_url: str = "http://localhost:8000"
    wombat_token_mode: str = "introspection"  # "introspection" | "jwt_secret"
    wombat_jwt_secret: str = ""
    wombat_refresh_token: str = ""
    wombat_refresh_threshold_seconds: int = 300

    mcp_host: str = "0.0.0.0"
    mcp_port: int = 3001

    log_level: str = "INFO"

    @field_validator("wombat_token_mode")
    @classmethod
    def _validate_token_mode(cls, value: str) -> str:
        value = value.lower()
        if value not in {"introspection", "jwt_secret"}:
            raise ValueError(
                "wombat_token_mode must be 'introspection' or 'jwt_secret'"
            )
        return value


settings = Settings()
