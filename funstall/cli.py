from functools import wraps

import click

from funstall.application_context import (
    ApplicationContext,
    create_application_context,
)
from funstall.config import Settings
from funstall.installation.installation import update, update_all
from funstall.packages import available_packages

# Command options


def package_name_option(f):
    return click.option(
        "--package",
        default=None,
        help="The name of a package",
    )(f)


# Options to modify Settings


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


def with_application_context(f):
    """Adds the application context to a CLI command.

    This decorator adds command options that modify common application
    settings. It then adds the application context (settings and services) to
    the decorated functions' arguments.
    """

    @package_file_url_option
    @verbosity_option
    @wraps(f)
    def g(
        *args,
        package_list_url: str | None,
        verbosity: str | None,
        **kwargs,
    ) -> None:
        settings_kwargs = {
            "package_file_url": package_list_url,
            "verbosity": verbosity,
        }
        settings = Settings.model_validate(
            {k: v for k, v in settings_kwargs.items() if v is not None}
        )
        ctx = create_application_context(settings)
        return f(*args, ctx=ctx, **kwargs)

    return g


@click.group()
def funstall():
    pass


@funstall.command("list")
@with_application_context
def list_packages(ctx: ApplicationContext) -> None:
    ctx["logger"].info("Available packages:")

    for p in available_packages():
        print(p.name)


@funstall.command("update")
@package_name_option
@with_application_context
def update_package(
    package: str | None,
    ctx: ApplicationContext,
) -> None:
    if package:
        update(ctx, package)
    else:
        update_all(ctx)
