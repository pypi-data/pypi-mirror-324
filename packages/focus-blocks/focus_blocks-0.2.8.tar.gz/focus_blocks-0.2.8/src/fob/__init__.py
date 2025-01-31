# This is the main entry point for the application.
import sys
import argparse

from rich import print

import fob.commands
from fob.utils import check_db_exists, get_db_path
from fob.db import TinyDBWrapper

def main():
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n[red bold]Exiting.[/red bold]")
        sys.exit(1)

def run_app():
    if len(sys.argv) == 1:
        print(
            '''[red][bold]Incorrect usage.[/bold][/red]

[cyan][bold]Usage:[/bold][/cyan] [green][bold]fob[/bold] [OPTIONS] <command>[/green]

Try [green][bold]fob help[/green][/bold] for usage information.
'''
        )
        sys.exit(1)

    # use our custom help page `fob help` instead of default argparse (`-h` or `--help`)
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        fob.commands.help(None, None)
        sys.exit(0)

    parser = argparse.ArgumentParser(
        prog="fob",
        description="A personal month-level daily block scheduler.",
        add_help=False,  # because we're using our own help page'
    )
    parser.add_argument(
        "-d", "--database", type=str, help="Optional custom path to database file."
    )
    parser.add_argument(
        "-x", "--debug", action="store_true", help="Enable debug mode."
    )
    subparsers = parser.add_subparsers(dest="command", help="Common Commands")
    subparsers.add_parser("help", help="Show help information and quit")
    subparsers.add_parser("new_month", help="Allocate blocks for a new month")
    subparsers.add_parser(
        "gm", help="Start a new day by selecting the blocks you will work on today"
    )
    subparsers.add_parser("reset", help="Reset fob by deleting persistent database file.")
    subparsers.add_parser("sup", help="Quick look at the month and today's blocks")
    did_parser = subparsers.add_parser("did", help="Check off blocks from today's checklist")
    did_parser.add_argument(
        "block_id",
        type=str,
        help="ID of the block to check off (int)",
    )
    didnt_parser = subparsers.add_parser("didnt", help="Revise block assignment for today and change a non-Buffer block into a Buffer block, and mark that new Buffer block as complete.")
    didnt_parser.add_argument(
        "block_id",
        type=str,
        help="ID of the block to convert to a Buffer block and check off (int)",
    )

    subparsers.add_parser("info", help="Show information about this program")
    args = parser.parse_args()

    if args.command is None:
        print("[red bold]Error:[/red bold] No command provided.")
        print("\nTry [green][bold]fob help[/bold][/green] for usage information.")
        return

    command_func = None
    try:
        command_func = getattr(fob.commands, args.command)
    except AttributeError:
        print(
            f"[red bold]fob {args.command}[/red bold] is not a valid fob command.\nSee [green bold]fob help[/green bold] for usage information."
        )
        sys.exit(1)

    db_path = get_db_path(args)
    if check_db_exists(args):
        if args.debug:
            print(f"Using [bold]existing[/bold] database at [not bold][magenta]{db_path}[/not bold][/magenta]")
    else:
        print(
            f"\N{WHITE HEAVY CHECK MARK} [bold]Created[/bold] new database at [not bold][magenta]{db_path}[/not bold][/magenta]"
        )
    db = TinyDBWrapper(db_path)

    command_func(args, db)

if __name__ == "__main__":
    main()
