from typing import Annotated, Literal

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


class PipConfig(BaseModel):
    name: str
    python_version: str
    executables: list[str]


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
