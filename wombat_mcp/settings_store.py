"""Load and save per-user MCP configuration.

The stdio server is normally configured through environment variables, but
local desktop users should not have to edit JSON configs by hand. This module
stores the API base URL, tokens, and related settings in the user's config
directory and makes them available to the bridge through ``os.environ`` and
the runtime ``Settings`` object.
"""
from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir
from pydantic import BaseModel, Field, field_validator

from wombat_mcp.compat import legacy_config_dir, warn_legacy

_CONFIG_DIR = Path(user_config_dir("wombat-mcp", appauthor=False))
_CONFIG_FILE = _CONFIG_DIR / "settings.json"
_LEGACY_CONFIG_FILE = legacy_config_dir() / "settings.json"


class UserConfig(BaseModel):
    """Persisted user settings for the stdio MCP server."""

    api_base_url: str = Field(default="http://localhost:8000")
    access_token: str = Field(default="")
    refresh_token: str = Field(default="")
    username: str = Field(default="")
    token_mode: str = Field(default="introspection")
    log_level: str = Field(default="INFO")

    @field_validator("token_mode")
    @classmethod
    def _validate_token_mode(cls, value: str) -> str:
        value = value.lower()
        if value not in {"introspection", "jwt_secret"}:
            raise ValueError(
                "token_mode must be 'introspection' or 'jwt_secret'"
            )
        return value

    def apply_to_env(self) -> None:
        """Copy non-empty values into environment variables."""
        env_map: dict[str, str] = {
            "WOMBAT_API_BASE_URL": self.api_base_url,
            "WOMBAT_ACCESS_TOKEN": self.access_token,
            "WOMBAT_REFRESH_TOKEN": self.refresh_token,
            "WOMBAT_TOKEN_MODE": self.token_mode,
            "WOMBAT_LOG_LEVEL": self.log_level,
        }
        for env_name, value in env_map.items():
            if value:
                os.environ[env_name] = value


def config_dir() -> Path:
    """Return the directory that holds the user's MCP settings."""
    return _CONFIG_DIR


def config_file() -> Path:
    """Return the path to the user's MCP settings file."""
    return _CONFIG_FILE


def load_user_config() -> UserConfig | None:
    """Load the user's persisted configuration, if it exists.

    Falls back to the deprecated WAFpass-era config file when the new one has
    not been written yet.
    """
    path = _CONFIG_FILE
    if not path.exists() and _LEGACY_CONFIG_FILE.exists():
        warn_legacy(str(_LEGACY_CONFIG_FILE), replacement=str(_CONFIG_FILE))
        path = _LEGACY_CONFIG_FILE
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    try:
        return UserConfig.model_validate(raw)
    except Exception:
        return None


def save_user_config(config: UserConfig) -> None:
    """Persist the configuration and restrict read access to the owner."""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = config.model_dump()
    _CONFIG_FILE.write_text(
        json.dumps(data, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    # Best-effort: keep tokens readable only by the owner.
    with contextlib.suppress(OSError):
        os.chmod(_CONFIG_FILE, 0o600)
