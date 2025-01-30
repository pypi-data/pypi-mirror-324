# main.py
import click

@click.group()
def cli():
    """🔥 This is a command line tool and it's mine.🔥"""
    pass

@cli.command()
@click.argument('name') # This positional argument bwill be passed to the function
def hello(name):
    """Prints a message to the console."""
    click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    cli()