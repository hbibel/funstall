import click

from funstall.packages import available_packages


@click.group()
def funstall():
    pass
    # raise click.UsageError("No arguments provided")


@funstall.command("list")
def list_packages() -> None:
    for p in available_packages():
        print(p.name)
