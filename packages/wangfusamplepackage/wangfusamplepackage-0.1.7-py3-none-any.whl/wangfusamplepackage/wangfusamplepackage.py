# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete

from .logging_config import setup_logging

# Set up logging once when the package is initialized
logger = setup_logging()


def start():
    print("Starting the application...")

def restart():
    print("Restarting the application...")


def main():
    parser = argparse.ArgumentParser(description="Manager my package")
    # parser.add_argument("--version", action="store_true", help="Show the package version")

    # Define commands
    parser.add_argument(
        "command", choices=["start", "stop", "restart"], help="Command to execute"
    )
    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.set_defaults(func=start)

    restart_parser = subparsers.add_parser("restart", help="Restart the application")
    restart_parser.set_defaults(func=restart)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    print(f"Executing {args.command}...")
