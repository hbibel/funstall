import os
import sys
from pathlib import Path


def user_data_dir() -> Path:
    """Directory for application data, such as databases or assets"""

    # inspired by
    # https://github.com/tox-dev/platformdirs/

    if data_home := os.getenv("XDG_DATA_HOME", "").strip():
        return Path(data_home) / "funstall"

    if sys.platform == "linux":
        return Path.home() / ".local" / "share" / "funstall"

    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "funstall"

    elif sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "funstall" / "data"

    else:
        msg = f"OS / platform {sys.platform} is not supported"
        raise ValueError(msg)


def user_config_file_dir() -> Path:
    """Contains settings file(s) for funstall"""

    # inspired by
    # https://github.com/tox-dev/platformdirs/

    if xdg := os.getenv("XDG_CONFIG_HOME", "").strip():
        return Path(xdg) / "funstall"

    if sys.platform == "linux":
        return Path.home() / ".config" / "funstall"

    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Preferences" / "preferences"

    elif sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "funstall" / "config"

    else:
        msg = f"OS / platform {sys.platform} is not supported"
        raise ValueError(msg)
