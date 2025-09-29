import click

from funstall.packages import available_packages


@click.group()
def funstall():
    pass


@funstall.command("list")
def list_packages() -> None:
    for p in available_packages():
        print(p.name)
