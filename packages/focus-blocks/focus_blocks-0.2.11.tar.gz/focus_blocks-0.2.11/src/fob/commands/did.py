from rich.pretty import pprint
from rich import print

from fob.commands.overviews import display_checklist
from fob.db import checklist_complete


def did(args, db):
    '''
    Usage: fob did <number>

    Check off a block from the day's checklist.

    The user is expected to run `fob sup` prior to running this command,
    which displays the month overview and the day's checklist.
    Then, the user can run `fob did <number>` to mark a the numbered block as completed.
    This command displays the updated checklist after marking the block as completed.
    Visually, it would exactly replace where the day's checklist was previously displayed,
    making it look like it was a GUI refresh.

    args.block_id: str - contains the block number to mark as completed.
    '''
    try:
        checklist = db.all()[0]['checklist']
    except IndexError:
        print("[red][bold]No day data found.[/red][/bold]")
        print("Run [green][bold]fob gm[/green][/bold] to start a new day.")
        return
    if args.debug:
        print("Checklist from DB:")
        pprint(checklist)

    if checklist_complete(db):
        print("\n[green]All blocks have already been completed.[/green] No changes made.")
        print("Start a new day: [green][bold]fob gm[/green][/bold]")
        return

    # check that the block_id is within range
    try:
        checklist[args.block_id].update({"done": True})
    except KeyError:
        print("[red][bold]Invalid block number.[/red][/bold]")
        return

    db.update({"checklist": checklist}, None)

    if args.debug:
        print("Updated checklist:")
        pprint(checklist)

    # display updated checklist
    display_checklist(args, db)


    if checklist_complete(db):
        print("[green]All blocks have been completed![/green]")
        print("Start a new day: [green][bold]fob gm[/green][/bold]")
        return
    else:
        print("[green]Checklist updated.[/green] See overview: [green][bold]fob sup[/green][/bold]")
