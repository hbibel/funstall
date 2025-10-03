import shutil
from logging import Logger
from textwrap import indent
from typing import TypedDict

from funstall.config import Settings
from funstall.installation.model import InstallError
from funstall.packages.model import PacmanPackage
from funstall.proc_utils import execute


class UpdateContext(TypedDict):
    logger: Logger
    settings: Settings


def _run_pacman_install(
    ctx: UpdateContext,
    package: PacmanPackage,
) -> tuple[bool, int, str]:
    if shutil.which("pacman") is None:
        raise InstallError(
            "The 'pacman' command was not found on the system's PATH."
        )

    cmd = [
        "sudo",
        "pacman",
        "-S",
        "--noconfirm",
        package.config.name,
    ]
    return execute(ctx, cmd)


def install(
    ctx: UpdateContext,
    package: PacmanPackage,
) -> None:
    success, exit_code, output = _run_pacman_install(ctx, package)

    if not success:
        msg = (
            f"Failed to install {package.config.name}, pacman process "
            f"returned {exit_code}. Process output:\n"
            f"{indent(output, '    ')}"
        )
        raise InstallError(msg)


def update(
    ctx: UpdateContext,
    package: PacmanPackage,
) -> None:
    success, exit_code, output = _run_pacman_install(ctx, package)

    if not success:
        msg = (
            f"Failed to update {package.config.name}, pacman process "
            f"returned {exit_code}. Process output:\n"
            f"{indent(output, '    ')}"
        )
        raise InstallError(msg)
