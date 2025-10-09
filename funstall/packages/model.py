from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import (
    ConfigDict,
    Field,
)


class BaseModel(_BaseModel):
    model_config = ConfigDict(extra="forbid")


class PackageData(BaseModel):
    version: int
    packages: list[Package]


class Package(BaseModel):
    name: str
    sources: list[PackageSource]
    dependencies: list[Dependency] | None = None


type PackageSource = Annotated[
    PacmanDef | PipDef | BrewDef, Field(discriminator="kind")
]


class PipDef(BaseModel):
    kind: Literal["pip"]
    config: PipConfig


class PipConfig(BaseModel):
    name: str
    python_version: str
    executables: list[str]


class PacmanDef(BaseModel):
    kind: Literal["pacman"]
    config: PacmanConfig


class PacmanConfig(BaseModel):
    name: str


class BrewDef(BaseModel):
    kind: Literal["brew"]
    config: PacmanConfig


class BrewConfig(BaseModel):
    name: str


class Dependency(BaseModel):
    name: str
    condition: DisplayServerCondition | PackageManagerCondition | None = Field(
        discriminator="kind", default=None
    )


class PackageManagerCondition(BaseModel):
    kind: Literal["package-manager"]
    is_: str = Field(alias="is")


class DisplayServerCondition(BaseModel):
    kind: Literal["display-server"]
    is_: str = Field(alias="is")


class PackageError(Exception):
    pass


class InvalidPackageFileError(PackageError):
    pass
