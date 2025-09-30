from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    package_file_url: HttpUrl = HttpUrl(
        "https://raw.githubusercontent.com/"
        "hbibel/funstall/refs/heads/main/packages.yaml"
    )
    # TODO package definitions file
