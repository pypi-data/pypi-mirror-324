import click
from .deploy import push_directory, run_directory
import os

@click.group()
def cli():
    """Simplex CLI tool"""
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))  
def push(directory):
    try:
        push_directory(directory)
    except Exception as e:
        print(f"Error running job: {e}")
        raise
    
    

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def run(directory):
    try:
        run_directory(directory)
    except Exception as e:
        print(f"Error running job: {e}")
        raise

def main():
    cli() 