from argparse import Namespace
from datetime import date

from rich.pretty import Pretty
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from tinydb import where, Query

from fob.db import TinyDBWrapper, checklist_complete
from fob.commands.overviews import month_overview, display_checklist

class InvalidUserInput(Exception):
    '''
    This exception should be raised if the user input is invalid.
    This exception implies that no changes were made to the database.
    '''
    pass

def gm(args: Namespace, db: TinyDBWrapper) -> None:
    '''
    Assign blocks to the current day, selecting from remaining blocks for the month.
    '''
    today = date.today()
    data = db.search(where('year') == today.year and where('month') == today.month)

    if len(data) == 0:
        print("[red][bold]No month data found.[/red][/bold]")
        print("Please run [green]fob new_month[/green] to create a new month of blocks.")
        return
    if len(data) > 1:
        print("[red][bold]Error![/red] More than one entry for the month has been found. This is a bug in the program. Please report it.")
        print("In the meantime, consider running [green]fob reset[/green].")
        return

    print("Good morning! \N{SUNRISE}")
    month_overview(args, db)
    try:
        new_day(args, db, data[0]) # can raise InvalidUserInput

    except InvalidUserInput:
        print("No changes were made to the database.")
        return

    # print("\n[green]Day successfully updated.[/green]")
    month_overview(args, db)

    print("[bold]Today's Checklist:[/bold]")
    display_checklist(args, db)

    print("[green]New day started.[/green]")
    print("See overview: [green]fob sup[/green]")
    print("Mark a block as done: [green]fob did [not bold]<number>[/not bold][/green]")
    print("Convert a block to Buffer: [green]fob didnt [not bold]<number>[/not bold][/green]")


def new_day(args: Namespace, db: TinyDBWrapper, data) -> None:
    if data['work_days_completed'] >= data['work_days_allocated']:
        print("\n[green]All work days have been completed for this month. Great job![/green]\n")
        print("Start a new month: [green][bold]fob new_month[/green][/bold]")
        return

    if Prompt.ask("Assign blocks to this new day?", choices=["yes", "no"], default="yes" if checklist_complete(db) else "no") == "no":
        print("Cancelled.")
        return


    today = date.today()
    print(f"You have [bold][cyan]{data['blocks_per_day']}[/bold][/cyan] blocks to assign today.\n")

    # will be updated
    not_completed_areas = {area: blocks for area, blocks in data['areas'].items() if blocks['completed'] < blocks['allocated']}

    # will not be updated
    completed_areas = {area: blocks for area, blocks in data['areas'].items() if blocks['completed'] >= blocks['allocated']}

    if args.debug:
        print("Not completed areas:")
        print(Panel(Pretty(not_completed_areas)))
        print("Completed areas:")
        print(Panel(Pretty(completed_areas)))

    new_not_completed_areas= {}
    today_areas = {}
    blocks_remaining_to_assign = data['blocks_per_day']
    blocks_per_day = data['blocks_per_day']

    for area_name, blocks in not_completed_areas.items():
        max_blocks = min(
            blocks['allocated'] - blocks['completed'],
            blocks_remaining_to_assign
        )
        blocks_assigned = int(Prompt.ask(f"({blocks_per_day - blocks_remaining_to_assign + 1}/{blocks_per_day}) How many blocks for [bold]{area_name}[/bold]? (max: [bold][cyan]{max_blocks}[/bold][/cyan])", default=0))

        if blocks_assigned > blocks_remaining_to_assign:
            print("[red][bold]Error![/red] You have assigned more blocks than you have available today. Please try again.")
            raise InvalidUserInput

        if blocks_assigned > blocks['allocated'] - blocks['completed']:
            print("[red][bold]Error![/red][/bold] You have assigned more blocks than are remaining in this area. Please try again.")
            raise InvalidUserInput

        blocks_remaining_to_assign -= blocks_assigned

        new_not_completed_areas[area_name] = {
            'allocated': blocks['allocated'],
            'completed': blocks['completed'] + int(blocks_assigned)
        }
        today_areas[area_name] = blocks_assigned

    if blocks_remaining_to_assign > 0:
        print("[red][bold]Error![/red][/bold] You have not assigned all your blocks. Please try again.")
        raise InvalidUserInput

    if args.debug:
        print("\nUpdates to be committed to the database:")
        print(Panel(Pretty(new_not_completed_areas)))
        print("Unchanged areas (completed before today):")
        print(Panel(Pretty(completed_areas)))

    not_completed_areas.update(new_not_completed_areas) # put back into 'not_completed_areas' areas which were not updated (0 blocks to do today)

    q = Query()
    combined_areas = {**not_completed_areas, **completed_areas}
    db.update({"areas": combined_areas}, q.year == today.year and q.month == today.month)
    db.update({"work_days_completed": data['work_days_completed'] + 1}, q.year == today.year and q.month == today.month)
    if args.debug:
        print("Database updated successfully.")
        print(Panel(Pretty(db.search(q.year == today.year and q.month == today.month))))

    checklist = dict()
    i = 0
    for area_name, blocks in today_areas.items():
        for _ in range(blocks):
            checklist[f"{i+1}"] = {"name": area_name, "done": False}
            i += 1


    db.update({"checklist": checklist}, None)

    if args.debug:
        print("Today's data:")
        print(Panel(Pretty(checklist)))
