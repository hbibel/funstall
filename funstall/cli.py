import click


@click.command()
def funstall():
    raise click.UsageError("No arguments provided")
