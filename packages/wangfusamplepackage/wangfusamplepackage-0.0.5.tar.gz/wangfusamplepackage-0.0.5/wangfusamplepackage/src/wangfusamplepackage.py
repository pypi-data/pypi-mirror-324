import argparse
import argcomplete


def start():
    print("Starting the application...")

def restart():
    print("Restarting the application...")


def main():
    parser = argparse.ArgumentParser(description="Manager my package")

    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser("start", help="Start the application")
    start_parser.set_defaults(func=start)

    restart_parser = subparsers.add_parser("restart", help="Restart the application")
    restart_parser.set_defaults(func=restart)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    args.func()

if __name__ == "__main__":
    main()