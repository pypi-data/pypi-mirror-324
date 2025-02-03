#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK 

import argparse
import argcomplete

from .logging_config import setup_logging

# Set up logging once when the package is initialized
logger = setup_logging()


def install():
    print("install the application...")

def update():
    print("update the application...")


def main():
    parser = argparse.ArgumentParser(description="Manager my package")
    # parser.add_argument("--version", action="store_true", help="Show the package version")

    # Define commands
    parser.add_argument(
        "command", choices=["install", "uninstall", "update"], help="Command to execute"
    )
    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser("install", help="Start the application")
    start_parser.set_defaults(func=install)

    restart_parser = subparsers.add_parser("update", help="update the application")
    restart_parser.set_defaults(func=update)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    print(f"Executing {args.command}...")
