from logging import Logger
from textwrap import indent
from typing import TypedDict

from funstall.installation.model import InstallError
from funstall.packages.model import BrewDef
from funstall.proc_utils import execute


class UpdateContext(TypedDict):
    logger: Logger


def install(
    ctx: UpdateContext,
    package_name: str,
    brew_definition: BrewDef,
) -> None:
    cmd = ["brew", "install"]
    if brew_definition.config.cask:
        cmd.append("--cask")
    cmd.append(brew_definition.config.name)

    success, _, output = execute(ctx, cmd)
    if not success:
        msg = f"""
            Failed to install {package_name}. Brew output:
            \n{indent(output, "    ")}
        """
        raise InstallError(msg)


def update(
    ctx: UpdateContext,
    package_name: str,
    brew_definition: BrewDef,
) -> None:
    cmd = ["brew", "upgrade"]
    if brew_definition.config.cask:
        cmd.append("--cask")
    cmd.append(brew_definition.config.name)

    success, _, output = execute(ctx, cmd)
    if not success:
        msg = f"""
            Failed to update {package_name}. Brew output:
            \n{indent(output, "    ")}
        """
        raise InstallError(msg)
