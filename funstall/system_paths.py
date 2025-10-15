import os
import sys
from logging import Logger
from pathlib import Path
from typing import TypedDict


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
        return Path.home() / "Library" / "Preferences" / "funstall"

    elif sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "funstall" / "config"

    else:
        msg = f"OS / platform {sys.platform} is not supported"
        raise ValueError(msg)


def user_exe_dir() -> Path:
    """Contains user-installed executables/binaries"""

    if xdg := os.getenv("XDG_BIN_HOME", "").strip():
        bin_dir = Path(xdg) / "funstall"

    elif sys.platform == "linux":
        bin_dir = Path.home() / ".local" / "bin"

    elif sys.platform == "darwin":
        bin_dir = Path.home() / "bin"

    elif sys.platform == "win32":
        bin_dir = Path.home() / "AppData" / "Local" / "funstall" / "bin"

    else:
        msg = f"OS / platform {sys.platform} is not supported"
        raise ValueError(msg)

    return bin_dir


class _WarnIfExeNotOnPathCtx(TypedDict):
    logger: Logger


def warn_if_exe_dir_not_on_path(ctx: _WarnIfExeNotOnPathCtx) -> None:
    if os_path := os.environ.get("PATH"):
        on_path = False
        d = str(user_exe_dir().resolve())
        for p in os_path.split(os.pathsep):
            if str(Path(p).resolve()) == d:
                on_path = True
                break

        if not on_path:
            ctx["logger"].warning(
                f"The user binary directory '{d}' is not found in the "
                "system's PATH. You may need to add it manually to run "
                "executables installed here."
            )
