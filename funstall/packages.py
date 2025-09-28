import os
import sys
from functools import cache
from pathlib import Path
from typing import Literal

import yaml  # type:ignore[import-untyped]
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field


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


class Package(BaseModel):
    name: str
    pacman: PacmanConfig
    dependencies: list[Dependency] | None = Field(default=None)


class PackageData(BaseModel):
    packages: list[Package]
    lists: dict[str, list[str]]


def available_packages() -> list[Package]:
    return [p for p in _package_data().packages]


@cache
def _package_data() -> PackageData:
    packages_file_content = (_appdata_dir() / "packages.yaml").read_text()
    data = yaml.safe_load(packages_file_content)

    return PackageData.model_validate(data)


def _appdata_dir() -> Path:
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

    return data_path / "funstall"
