import click

from funstall.application_context import create_application_context
from funstall.config import Settings
from funstall.installation.installation import update, update_all
from funstall.packages import available_packages


def package_name_option(f):
    return click.option(
        "--package",
        default=None,
        help="The name of a package",
    )(f)


def package_file_url_option(f):
    return click.option(
        "--package-list-url",
        default=None,
        help="URL to the package list file to use",
    )(f)


def verbosity_option(f):
    return click.option(
        "--verbosity",
        default=None,
        help=(
            "Configure informative messages which will be written to stderr. "
            "May be set to 'silent', 'error', 'info', or 'debug'. Default is "
            "'info'."
        ),
    )(f)


@click.group()
def funstall():
    pass


@funstall.command("list")
@verbosity_option
def list_packages(verbosity: str | None) -> None:
    settings_kwargs = {
        "verbosity": verbosity,
    }
    settings = Settings.model_validate(
        {k: v for k, v in settings_kwargs.items() if v is not None}
    )
    ctx = create_application_context(settings)

    ctx["logger"].info("Available packages:")

    for p in available_packages():
        print(p.name)


# TODO consolidate some of these decorators to e.g. common_settings_options and
# application_context
@funstall.command("update")
@package_name_option
@package_file_url_option
@verbosity_option
def update_package(
    package: str | None,
    package_list_url: str | None,
    verbosity: str | None,
) -> None:
    settings_kwargs = {
        "package_file_url": package_list_url,
        "verbosity": verbosity,
    }
    settings = Settings.model_validate(
        {k: v for k, v in settings_kwargs.items() if v is not None}
    )
    ctx = create_application_context(settings)

    if package:
        update(ctx, package)
    else:
        update_all(ctx)
