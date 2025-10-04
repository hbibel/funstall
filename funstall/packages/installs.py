import tomllib
from logging import Logger
from pathlib import Path
from typing import TypedDict

import tomli_w
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict

from funstall import system_paths
from funstall.packages.model import Package


class BaseModel(_BaseModel):
    model_config = ConfigDict(extra="forbid")


class PackageInstalls(BaseModel):
    installed: list[str]


class AddInstalledContext(TypedDict):
    logger: Logger


def is_installed(package: Package) -> bool:
    return package.name in _load_installs().installed


def add_installed(ctx: AddInstalledContext, package: Package) -> None:
    ctx["logger"].debug("Adding %s to installed packages", package.name)

    if is_installed(package):
        ctx["logger"].warning(
            (
                "Package %s is already installed, not adding again to the "
                "installed list"
            ),
            package.name,
        )
        return

    installs = _load_installs()
    installs.installed.append(package.name)
    new_content = tomli_w.dumps(installs.model_dump())
    _installed_packages_file().write_text(new_content)


def _installed_packages_file() -> Path:
    installs_file = system_paths.user_data_dir() / "installed.toml"

    if not installs_file.parent.exists():
        installs_file.parent.mkdir(parents=True)
    if not installs_file.exists():
        installs_file.write_text("installed=[]")

    return installs_file


def _load_installs() -> PackageInstalls:
    installs_file = _installed_packages_file()
    content = tomllib.loads(installs_file.read_text())
    return PackageInstalls.model_validate(content)
