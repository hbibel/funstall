from enum import StrEnum
from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from funstall import system_paths


class Verbosity(StrEnum):
    SILENT = "silent"
    ERROR = "error"
    INFO = "info"
    DEBUG = "debug"


class Settings(BaseSettings):
    package_file_url: HttpUrl = HttpUrl(
        "https://raw.githubusercontent.com/"
        "hbibel/funstall/refs/heads/main/packages.yaml"
    )
    base_installation_dir: Path = system_paths.user_data_dir() / "packages"
    package_definitions_file: Path = (
        system_paths.user_data_dir() / "packages.yaml"
    )
    verbosity: Verbosity = Verbosity.INFO

    model_config = SettingsConfigDict(
        toml_file=system_paths.user_config_file_dir() / "config.toml"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            TomlConfigSettingsSource(settings_cls),
        )
