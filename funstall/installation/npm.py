import os
import shutil
import stat
from logging import Logger
from pathlib import Path
from textwrap import indent
from typing import TypedDict

from funstall.config import Settings
from funstall.installation.model import InstallError
from funstall.packages.model import NpmDef
from funstall.proc_utils import execute


class _InstallContext(TypedDict):
    logger: Logger
    settings: Settings


def install(
    ctx: _InstallContext,
    package_name: str,
    npm_definition: NpmDef,
) -> None:
    # Node package setup
    # install-dir
    # |- node/bin/node
    # |- node_modules/.bin/the_package
    # |- package.json

    installation_dir = ctx["settings"].base_installation_dir / package_name
    node_version = npm_definition.config.node_version

    try:
        installation_dir.mkdir()
    except FileExistsError:
        if os.listdir(installation_dir):
            msg = f"Installation directory {installation_dir} is not empty"
            raise InstallError(msg)

    _install_node(ctx, installation_dir, node_version)
    _install_package(ctx, installation_dir, npm_definition)


class _LoggerContext(TypedDict):
    logger: Logger


def _install_node(
    ctx: _LoggerContext,
    installation_dir: Path,
    version: str,
) -> None:
    ctx["logger"].debug("Installing Node to %s", installation_dir)
    success, _, output = execute(
        ctx,
        [
            "fnm",
            "--fnm-dir",
            installation_dir.__str__(),
            "install",
            version,
        ],
    )
    if not success:
        msg = (
            f"Installation of Node version '{version}' failed:\n"
            f"{indent(output, '  ')}"
        )
        raise InstallError(msg)

    version_dir_parent = installation_dir / "node-versions"
    ctx["logger"].debug(
        "Installation dir content: %s",
        ", ".join(os.listdir(version_dir_parent)),
    )
    version_dir_name = next(
        d
        for d in os.listdir(version_dir_parent)
        if d.startswith("v" + version)
    )
    ctx["logger"].debug("Node is installed in %s", version_dir_name)
    shutil.move(
        version_dir_parent / version_dir_name / "installation",
        installation_dir / "node",
    )


def _install_package(
    ctx: _InstallContext,
    installation_dir: Path,
    npm_definition: NpmDef,
) -> None:
    packages = [
        npm_definition.config.name,
        *(npm_definition.config.additional_packages or []),
    ]

    npm_cmd, env = _npm_cmd_and_env(installation_dir)
    success, exit_code, output = execute(
        ctx,
        [
            npm_cmd,
            "add",
            *packages,
        ],
        working_dir=installation_dir,
        env=env,
    )
    if not success:
        msg = (
            f"NPM install for package {npm_definition.config.name} failed:\n"
            f"{indent(output, '    ')}"
        )
        raise InstallError(msg)

    for exe in npm_definition.config.executables:
        _create_launch_script(
            ctx["settings"].bin_dir / exe, installation_dir, exe
        )


def _create_launch_script(
    script_path: Path, installation_dir: Path, executable: str
) -> None:
    # Executables from npm packages usually are node scripts, with a
    # `#!/usr/bin/env node` statement on top, so the right node version
    # needs to be on PATH. Hence we create this wrapper script instead of just
    # linking the executable
    add_path = os.pathsep.join(
        str(p)
        for p in (
            installation_dir / "node_modules" / ".bin",
            installation_dir / "node" / "bin",
        )
    )
    executable_path = installation_dir / "node_modules" / ".bin" / executable
    script = "\n".join(
        [
            "#!/bin/sh",
            "",
            f"PATH=$PATH{os.pathsep}{add_path} {executable_path}",
        ]
    )
    script_path.write_text(script)

    current_mode = os.stat(script_path).st_mode
    new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP
    os.chmod(script_path, new_mode)


class _UpdateContext(TypedDict):
    logger: Logger
    settings: Settings


def update(
    ctx: _UpdateContext,
    package_name: str,
    npm_definition: NpmDef,
) -> None:
    installation_dir = ctx["settings"].base_installation_dir / package_name

    packages = [
        npm_definition.config.name,
        *(npm_definition.config.additional_packages or []),
    ]
    npm_cmd, env = _npm_cmd_and_env(installation_dir)
    success, exit_code, output = execute(
        ctx,
        [
            npm_cmd,
            "update",
            *packages,
        ],
        working_dir=installation_dir,
        env=env,
    )
    if not success:
        msg = (
            f"NPM update for package {npm_definition.config.name} failed:\n"
            f"{indent(output, '    ')}"
        )
        raise InstallError(msg)


def _npm_cmd_and_env(installation_dir: Path) -> tuple[str, dict[str, str]]:
    path_with_node = (
        os.getenv("PATH", "")
        + os.pathsep
        + (installation_dir / "node" / "bin").resolve().__str__()
    )
    return (
        (installation_dir / "node" / "bin" / "npm").__str__(),
        {"PATH": path_with_node},
    )
