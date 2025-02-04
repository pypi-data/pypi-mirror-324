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

    parser = argparse.ArgumentParser(prog="boostedutocomplete CLI helper")

    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcommands
    subparsers.add_parser("start", help="start the application")
    subparsers.add_parser("restart", help="restart the applicatoin")
    subparsers.add_parser("stop", help="stop the application")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.subcommand == "start":
        start()
    elif args.subcommand == "restart":
        restart()
    elif args.subcommand == "stop":
        stop()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()