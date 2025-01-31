#! /usr/bin/env python3

import click
from sarif_manager.bin.logger import init_logger

from sarif_manager.version import __version__
from sarif_manager.command.azure import azure
from sarif_manager.command.slack import slack
from dotenv import load_dotenv

load_dotenv()


@click.group
@click.version_option(version=__version__)
def sarif_manager():
    """Parse and use SARIF files for security analysis."""
    init_logger()


sarif_manager.add_command(azure)
sarif_manager.add_command(slack)

def main():
    """Parse and use SARIF files for security analysis."""
    sarif_manager()


if __name__ == '__main__':
    main()
