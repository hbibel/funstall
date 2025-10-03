import os
import sys
from logging import Logger
from pathlib import Path
from typing import TypedDict

from funstall.config import SelfUpdateStrategy, Settings
from funstall.installation import pacman, pip
from funstall.installation.model import InstallError
from funstall.packages.installs import add_installed, is_installed
from funstall.packages.model import (
    Package,
    PackageError,
    PipConfig,
    PipPackage,
)
from funstall.packages.package_definitions import (
    get_package,
    update_package_definitions,
)


class InstallContext(TypedDict):
    settings: Settings
    logger: Logger


def install(ctx: InstallContext, package_name: str) -> None:
    _update_funstall(ctx)

    ctx["logger"].info("Installing package '%s'", package_name)

    pkg = get_package(ctx["settings"], package_name)
    if not pkg:
        msg = f"Package '{package_name}' not found"
        raise InstallError(msg)

    if is_installed(pkg):
        ctx["logger"].info("Package %s is already installed", pkg.name)

    if pkg.kind == "pip":
        pip.install(ctx, pkg)
    elif pkg.kind == "pacman":
        pacman.install(ctx, pkg)

    add_installed(ctx, pkg)


class UpdateContext(TypedDict):
    settings: Settings
    logger: Logger


def update(ctx: UpdateContext, package: str) -> None:
    _update_funstall(ctx)

    # TODO we have a chicken-and-egg problem here: If the schema changes,
    # how can this version of the code validate the new package file?
    # Maybe relaunch this program with the new file passed as packages
    # file, and replace the old file in the end

    # try:
    #   package_after = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageDeleted

    # if package_before.kind == package_after.kind
    #   use same strategy to update
    # else:
    #   remove old package
    #   install new package


def update_all(ctx: UpdateContext) -> None:
    # try:
    # package_before = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageNotFound

    _update_funstall(ctx)

    # try:
    #   package_after = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageDeleted

    # TODO handle packages that have been removed, prompt the user
    # for p in installed_packages():
    #     update(p)


def _update_funstall(ctx: UpdateContext) -> None:
    self_update_successful = True
    if ctx["settings"].skip_self_update:
        ctx["logger"].debug("Skipping self update")
    else:
        try:
            _update_self(ctx)
            ctx["logger"].debug("Self update complete")

            # Restart with new code
            args = sys.argv + ["--skip-self-update"]
            ctx["logger"].debug(
                "Restarting %s as `%s`",
                sys.executable,
                " ".join([sys.executable] + args),
            )
            for h in ctx["logger"].handlers:
                h.flush()
            os.execv(sys.executable, [sys.executable] + args)
        except InstallError as e:
            ctx["logger"].warning(
                "Self update failed, will not update package list" + e.msg
            )
            self_update_successful = False

    # If the self-update was not successful, we don't need to fail the
    # entire program, but we should not update the package list in case the
    # format has changed and our current version cannot handle the new format.
    if self_update_successful:
        ctx["logger"].info("Updating package list ...")
        try:
            update_package_definitions(ctx["settings"])
            ctx["logger"].debug("Package list updated")
        except PackageError as e:
            ctx["logger"].warning(
                "Could not update package list, continuing with old package "
                "definitions. This will lead to a crash if the new funstall "
                "version is not compatible with the old package list."
            )
            ctx["logger"].debug("Cause: %s", e)


def _update_self(ctx: UpdateContext) -> None:
    logger = ctx["logger"]

    logger.info("Updating funstall")

    if ctx["settings"].self_update_strategy == SelfUpdateStrategy.NOOP:
        logger.info("Noop update strategy")
    elif ctx["settings"].self_update_strategy == SelfUpdateStrategy.PYPI:
        logger.debug("Updating funstall using pip")
        pip_path = Path(sys.executable).parent / "pip"
        logger.debug(
            "funstall is installed at %s", str(pip_path.parent.parent)
        )

        p = PipPackage(
            name="funstall",
            kind="pip",
            config=PipConfig(
                name="funstall",
                python_version="3.13",
                executables=["funstall"],
            ),
        )
        pip.update(ctx, p, pip_bin=pip_path.__str__())


def _update_package(ctx: UpdateContext, package: Package) -> None:
    ctx["logger"].info("Updating funstall")
    if package.kind == "pip":
        p: PipPackage = package
        pip.update(ctx, p)
