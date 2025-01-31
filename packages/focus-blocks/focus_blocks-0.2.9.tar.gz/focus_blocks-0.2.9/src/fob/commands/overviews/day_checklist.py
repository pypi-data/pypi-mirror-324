from argparse import Namespace

from rich.pretty import pprint
from rich import print
from rich.panel import Panel

from fob.db import TinyDBWrapper

def display_checklist(args: Namespace, db: TinyDBWrapper) -> None:
    try:
        checklist = db.all()[0]['checklist']
    except (IndexError, KeyError):
        print("[red][bold]No day data found.[/red][/bold]")
        print("Run [green][bold]fob gm[/green][/bold] to start a new day.")
        return
    if args.debug:
        print("Checklist from DB:")
        pprint(checklist)
    # print the checklist
    for num, info in checklist.items():
        print(Panel(f"{num}: {info['name']}", border_style="bold green" if info['done'] else "bold red"))
