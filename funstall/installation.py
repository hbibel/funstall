from funstall.config import Settings
from funstall.packages import InvalidPackageFileError, update_package_list


class UpdateError(Exception):
    pass


def update(settings: Settings, package_name: str) -> None:
    # try:
    # package_before = packages.get(package_name)
    # except NoSuchPackage:
    #   raise PackageNotFound

    try:
        update_package_list(settings)
    except InvalidPackageFileError:
        raise UpdateError(
            "Can't update the package file list right now because the remote "
            "package file is not valid."
        )

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
