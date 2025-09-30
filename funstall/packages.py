import os
import sys
from pathlib import Path
from typing import Annotated, Literal

import httpx
import yaml  # type:ignore[import-untyped]
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field

from funstall.config import Settings


class BaseModel(_BaseModel):
    model_config = ConfigDict(extra="forbid")


class PackageManagerCondition(BaseModel):
    kind: Literal["package-manager"]
    is_: str = Field(alias="is")


class DisplayServerCondition(BaseModel):
    kind: Literal["display-server"]
    is_: str = Field(alias="is")


class Dependency(BaseModel):
    name: str
    condition: DisplayServerCondition | PackageManagerCondition | None = Field(
        discriminator="kind", default=None
    )


class PacmanConfig(BaseModel):
    name: str


class PipConfig(BaseModel):
    name: str


class BasePackage(BaseModel):
    name: str


class PipPackage(BasePackage):
    kind: Literal["pip"]

    config: PipConfig


class PacmanPackage(BasePackage):
    kind: Literal["pacman"]

    config: PacmanConfig
    dependencies: list[Dependency] | None = Field(default=None)


Package = Annotated[PacmanPackage | PipPackage, Field(discriminator="kind")]


class PackageData(BaseModel):
    packages: list[Package]
    lists: dict[str, list[str]]


class PackageError(Exception):
    pass


class InvalidPackageFileError(PackageError):
    pass


def available_packages() -> list[Package]:
    return [p for p in _package_data().packages]


def update_package_list(settings: Settings) -> None:
    new_content = httpx.get(str(settings.package_file_url)).text

    try:
        yaml.safe_load(new_content)
    except yaml.YAMLError:
        raise InvalidPackageFileError

    # Path.write_text overwrites a file
    _packages_file_path().write_text(new_content)


def _package_data() -> PackageData:
    packages_file_content = _packages_file_path().read_text()
    data = yaml.safe_load(packages_file_content)

    return PackageData.model_validate(data)


def _packages_file_path() -> Path:
    # inspired by
    # https://github.com/tox-dev/platformdirs/

    data_path: Path

    match sys.platform:
        case "linux":
            p = os.environ.get("XDG_DATA_HOME", "")
            if p.strip():
                data_path = Path(p).resolve()
            else:
                data_path = Path.home() / ".local" / "share"

        case "darwin":
            data_path = Path.home() / "Library" / "Application Support"

        case "win32":
            data_path = Path.home() / "AppData" / "Local"

        case other:
            msg = f"OS / platform {other} is not supported"
            raise ValueError(msg)

    return data_path / "funstall" / "packages.yaml"
