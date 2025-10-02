import sys
from logging import Logger
from pathlib import Path
from typing import TypedDict, overload

from funstall.config import Settings
from funstall.installation import pip
from funstall.installation.model import UpdateError
from funstall.packages import (
    InvalidPackageFileError,
    Package,
    PipConfig,
    PipPackage,
    update_package_list,
)


class UpdateContext(TypedDict):
    settings: Settings
    logger: Logger


@overload
def update(ctx: UpdateContext, package: str) -> None: ...


@overload
def update(ctx: UpdateContext, package: Package) -> None: ...


def update(ctx: UpdateContext, package: Package | str) -> None:
    try:
        _update_self(ctx)
        self_update_successful = True
    except UpdateError as e:
        ctx["logger"].warning(
            "Self update failed, will not update package list" + e.msg
        )
        self_update_successful = False

    # try:
    # package_before = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageNotFound

    # If the self-update was not successful, we can try and continue, but we
    # should not update the package list in case the format has changed and our
    # current version cannot handle the new format.

    if self_update_successful:
        ctx["logger"].info("Updating package list ...")
        # try:
        #     update_package_list(settings)
        # except InvalidPackageFileError:
        #     raise UpdateError(
        #         "Can't update the package file list right now because the remote "
        #         "package file is not valid."
        #     )

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
    try:
        _update_self(ctx)
        self_update_successful = True
    except UpdateError as e:
        ctx["logger"].warning(
            "Self update failed, will not update package list" + e.msg
        )
        self_update_successful = False

    # try:
    # package_before = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageNotFound

    # If the self-update was not successful, we can try and continue, but we
    # should not update the package list in case the format has changed and our
    # current version cannot handle the new format.

    if self_update_successful:
        ctx["logger"].info("Updating package list ...")
        # try:
        #     update_package_list(settings)
        # except InvalidPackageFileError:
        #     raise UpdateError(
        #         "Can't update the package file list right now because the remote "
        #         "package file is not valid."
        #     )

    # try:
    #   package_after = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageDeleted

    # TODO handle packages that have been removed, prompt the user
    # for p in installed_packages():
    #     update(p)


def _update_self(ctx: UpdateContext) -> None:
    logger = ctx["logger"]

    logger.info("Updating funstall")

    pip_path = Path(sys.executable).parent / "pip"
    logger.debug("funstall is installed at %s", str(pip_path.parent.parent))

    p = PipPackage(
        name="funstall", kind="pip", config=PipConfig(name="funstall")
    )
    pip.update(ctx, p, pip_bin=pip_path.__str__())


def _update_package(ctx: UpdateContext, package: Package) -> None:
    ctx["logger"].info("Updating funstall")
    if package.kind == "pip":
        p: PipPackage = package
        pip.update(ctx, p)
