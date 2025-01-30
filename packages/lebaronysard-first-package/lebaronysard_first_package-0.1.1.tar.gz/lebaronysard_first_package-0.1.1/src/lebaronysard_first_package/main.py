# main.py
import click
import subprocess

@click.group()
def cli():
    """🔥 This is a command line tool and it's mine.🔥"""
    pass

@cli.command()
@click.argument('name')
def hello(name):
    """Prints a message to the console."""
    click.echo("Hello "+click.style(f'{name}!', fg='green'))

if __name__ == '__main__':
    cli()
