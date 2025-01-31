from rich import print
from argparse import Namespace

from fob.db import TinyDBWrapper

def help(args: Namespace | None, db: TinyDBWrapper | None) -> None:
    '''
    Print detailed help / usage information for this program.
    '''
    print("""
[bold]Usage:[/bold] [green][bold]fob[/bold] [OPTIONS] COMMAND[/green]

A personal month-level daily block scheduler.

[cyan bold]Common Commands:[/cyan bold]
    [green bold]help[/green bold]        Show this help information.
    [green bold]info[/green bold]        Show information about this program.
    [green bold]new_month[/green bold]   Allocate blocks for a new month.
    [green bold]gm[/green bold]          Start a new day by selecting the blocks you will work on today.
    [green bold]sup[/green bold]         Quick look at the month and today's blocks.
    [green bold]did[/green bold]         Check off blocks from today's checklist.
    [green bold]didnt[/green bold]       Convert a block from today's checklist to to a 'Buffer' block.
    [green bold]reset[/green bold]       Delete persistent database file.

[cyan bold]Global Options:[/cyan bold]
    [green bold]-d, --database[/green bold] [magenta not bold]<PATH_TO_DB_FILE>[/magenta not bold]  Path to database file. You can use a cloud storage (eg. Dropbox) to sync the database across devices.
    [green bold]-x, --debug[/green bold]  Enable debug mode.

First time using fob? Start by running [green][bold]fob new_month[/green][/bold] to allocate blocks for the month.""")
