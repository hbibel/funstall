import subprocess
from logging import Logger
from textwrap import indent
from typing import TypedDict

from funstall.config import Settings
from funstall.installation.model import UpdateError
from funstall.packages import PipPackage


class UpdateContext(TypedDict):
    logger: Logger
    settings: Settings


def update(
    ctx: UpdateContext,
    package: PipPackage,
    *,
    pip_bin: str | None = None,
) -> None:
    # TODO:
    # Check if Python version is still supported; if not, recreate venv
    # Here's a fun little document to read for this
    # https://packaging.python.org/en/latest/specifications/version-specifiers/#id5
    # pip metadata for checking Python version: https://pypi.org/pypi/<package name>/json
    # https://pypi.org/pypi/funstall/json
    # -> key info.requires_python

    if not pip_bin:
        pip_bin = (
            (
                ctx["settings"].base_installation_dir
                / package.name
                / "bin"
                / "pip"
            )
            .resolve()
            .__str__()
        )

    cmd = [
        pip_bin,
        "install",
        "--upgrade",
        "--pre",
        package.config.name,
    ]

    ctx["logger"].debug("Invoking `%s`", " ".join(cmd))
    done = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if done.returncode != 0:
        output = done.stdout.decode(errors="ignore")
        msg = f"""
            Failed to update {package.config.name}, {pip_bin} process returned
            {done.returncode}. Pip output:
            \n{indent(output, "    ")}
        """
        raise UpdateError(msg)
    else:
        ctx["logger"].debug(
            "Pip output:\n%s", done.stdout.decode(errors="ignore")
        )
