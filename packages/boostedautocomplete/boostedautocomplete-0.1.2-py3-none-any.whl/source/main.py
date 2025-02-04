#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK 

import argparse
import argcomplete

def start():
    print("Starting the applicatoin...")
def restart():
    print("Restarting the application")
def stop():
    print("Stop the application.")


def main():

    # Handles autocomplete requests

    parser = argparse.ArgumentParser(prog="boostedutocomplete")
    parser.add_argument("command", choices=["start", "restart", "stop"], help="commands for autocomplete")
    subparsers = parser.add_subparsers()

    start_parser = subparsers.add_parser("start", help="start the appliation")
    start_parser.set_defaults(func=start)

    restart_parser = subparsers.add_parser("restart", help="restart the appliation")
    restart_parser.set_defaults(func=restart)

    stop_parser = subparsers.add_parser("stop", help="stop the appliation")
    stop_parser.set_defaults(func=stop)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    print(f"Executing {args.command}...")


if __name__ == "__main__":
    main()