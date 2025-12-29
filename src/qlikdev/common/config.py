from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple

from dotenv import dotenv_values
from qlik_sdk import AuthType, Config

DEFAULT_ENV_FILENAMES: Tuple[str, ...] = ("qlikcloud.env", ".env")


def _find_env_file(explicit: Optional[str] = None) -> Optional[Path]:
    """
    Locate an env file using (in order): an explicit path, QLIKDEV_ENV_FILE,
    the current working directory, and the package directory.
    """
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    if env_override := os.environ.get("QLIKDEV_ENV_FILE"):
        candidates.append(Path(env_override))

    cwd = Path.cwd()
    pkg_dir = Path(__file__).resolve().parent.parent
    for name in DEFAULT_ENV_FILENAMES:
        candidates.append(cwd / name)
        candidates.append(pkg_dir / name)

    for path in candidates:
        if path.is_file():
            return path
    return None


def build_config(env_file: Optional[str] = None) -> Config:
    """
    Create a qlik_sdk Config using an env file and/or environment variables.

    Priority:
    1) Values in the chosen env file
    2) Environment variables QCS_SERVER / QCS_API_KEY
    """
    env_path = _find_env_file(env_file)
    env_values = dotenv_values(dotenv_path=env_path) if env_path else {}

    host = env_values.get("QCS_SERVER") or os.environ.get("QCS_SERVER")
    api_key = env_values.get("QCS_API_KEY") or os.environ.get("QCS_API_KEY")

    if not host or not api_key:
        msg = "Missing QCS_SERVER or QCS_API_KEY."
        details = f" Looked in {env_path}" if env_path else " No env file found."
        raise ValueError(msg + details)

    return Config(host=host, auth_type=AuthType.APIKey, api_key=api_key)
