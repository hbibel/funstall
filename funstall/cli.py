import click

# from funstall.installation_strategies import platform, python, node
from funstall.installation_strategies import python  # TODO platform, node
from funstall.packages import available_packages


@click.group()
def funstall():
    pass


@funstall.command("list")
def list_packages() -> None:
    for p in available_packages():
        print(p.name)


@funstall.group("self")
def self_commands() -> None:
    pass


@self_commands.command()
def update() -> None:
    print("Updating funstall")
    python.update("funstall")
