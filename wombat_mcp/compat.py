"""Deprecated-name compatibility for the WAFpass → WOMBATpass migration.

Environment variables and the per-user config directory used the ``wafpass``
prefix before the rebrand. New installs use ``wombat``; legacy values are
still read (with a deprecation warning) for one migration window.
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path

ENV_PREFIX = "WOMBAT_"
LEGACY_ENV_PREFIX = "WAFPASS_"

LEGACY_CONFIG_APP_NAME = "wafpass-mcp"
CONFIG_APP_NAME = "wombat-mcp"

_promoted = False


def warn_legacy(what: str, *, replacement: str | None = None) -> None:
    """Emit a consistent deprecation warning for an old WAFpass name."""
    suffix = f" Use {replacement} instead." if replacement else ""
    warnings.warn(
        f"{what} is deprecated after the WAF++ → Wombat rebrand.{suffix}",
        FutureWarning,
        stacklevel=3,
    )


def _promote(mapping) -> None:  # noqa: ANN001 - os.environ-like mapping
    for key in list(mapping):
        if not key.startswith(LEGACY_ENV_PREFIX):
            continue
        new_key = ENV_PREFIX + key[len(LEGACY_ENV_PREFIX):]
        if new_key in mapping:
            continue
        mapping[new_key] = mapping[key]
        warn_legacy(f"Environment variable {key}", replacement=new_key)


def promote_legacy_env(env_file: str | Path = ".env") -> None:
    """Copy legacy ``WAFPASS_*`` settings to their ``WOMBAT_*`` names."""
    global _promoted
    if _promoted:
        return
    _promoted = True

    _promote(os.environ)

    path = Path(env_file)
    if not path.exists():
        return
    try:
        from dotenv import dotenv_values
    except ImportError:  # pragma: no cover - python-dotenv is a hard dependency
        return

    values = {k: v for k, v in dotenv_values(path).items() if v is not None}
    for key, value in values.items():
        if not key.startswith(LEGACY_ENV_PREFIX):
            continue
        new_key = ENV_PREFIX + key[len(LEGACY_ENV_PREFIX):]
        if new_key in os.environ or new_key in values:
            continue
        os.environ[new_key] = value
        warn_legacy(f"Environment variable {key} in {path}", replacement=new_key)


def legacy_config_dir() -> Path:
    """Return the WAFpass-era per-user config directory."""
    from platformdirs import user_config_dir

    return Path(user_config_dir(LEGACY_CONFIG_APP_NAME, appauthor=False))
