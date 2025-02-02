import argparse
import argcomplete
from wangfusamplepackage import __version__


def start():
    print("Starting the application...")

def restart():
    print("Restarting the application...")


def main():
    parser = argparse.ArgumentParser(description="Manager my package")
    parser.add_argument("--version", action="store_true", help="Show the version")

    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.set_defaults(func=start)

    restart_parser = subparsers.add_parser("restart", help="Restart the application")
    restart_parser.set_defaults(func=restart)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    args.func()
    if args.version:
        print(f"reef-autocomplete version {__version__}")

if __name__ == "__main__":
    main()