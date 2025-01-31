from argparse import Namespace
from os import remove, rmdir

from rich import print
from rich.prompt import Prompt

from fob.utils import get_db_path
from fob.db import TinyDBWrapper


def reset(args: Namespace, db: TinyDBWrapper) -> None:
    '''
    Delete currently used database and parent directory if it's named 'fob' and empty.
    '''
    db_path = get_db_path(args)

    print(f"[red bold]Warning![/red bold] This will delete the database file at [cyan][not bold]{db_path}[/cyan][/not bold]")

    if Prompt.ask("Are you sure?", choices=["yes", "no"], default="no") == "no":
        print("Reset cancelled.")
        return


    try:
        remove(db_path)
        print(f"\N{WHITE HEAVY CHECK MARK} [bold]Deleted[/bold] persistent database at [not bold][magenta]{db_path}[/not bold][/magenta].")
    except FileNotFoundError:
        pass
    try:
        if db_path.parent.name == 'fob':
            try:
                rmdir(db_path.parent)
                print(f"\N{WHITE HEAVY CHECK MARK} Also [bold]deleted[/bold] parent directory [cyan]'fob'[/cyan] at [not bold][cyan]{db_path.parent}[/not bold][/cyan].")
            except OSError:
                print(f"[red]Warning:[/red] Parent directory [yellow]{db_path.parent}[/yellow] was not deleted. You may want to delete it manually.")
        else:
            print(f"[red]Warning:[/red] Parent directory [yellow]{db_path.parent}[/yellow] was not deleted. You may want to delete it manually.")
    except FileNotFoundError:
        pass

    print("\nStart a new month: [green][bold]fob new_month[/green][/bold]")
