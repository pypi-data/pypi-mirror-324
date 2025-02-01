from argparse import Namespace
from datetime import date

from tinydb import where, Query
from rich.pretty import pprint
from rich import print
from rich.prompt import Prompt

from fob.commands.overviews.day_checklist import display_checklist
from fob.db.wrapper import TinyDBWrapper
from fob.db import checklist_complete


def didnt(args: Namespace, db: TinyDBWrapper):
    '''
    Usage: fob didnt <number>

    Convert a non-Buffer block into a Buffer block.
    Used instead of 'did' when a block was not completed due to unforeseen circumstances.
    '''
    today = date.today()
    try:
        data = db.search(where('year') == today.year and where('month') == today.month)[0]
    except IndexError:
        print("[red][bold]No month data found.[/red][/bold]")
        print("Run [green]fob new_month[/green] to start a new month.")
        return

    if args.debug:
        pprint(data)

    try:
        buffer_entry = data['areas']['Buffer']
    except KeyError:
        print("[red][bold]Program Error: Database seems to be malformed.[/red][/bold] (Database value at ['areas']['Buffer'] doesn't exist. Please report this issue. In the meantime, consider [green]fob reset[/green] to delete the database and start fresh.")
        return

    # guard: today's checklist is all completed
    if checklist_complete(db):
        print("[green][bold]All blocks for today are completed![/green][/bold]")
        print("Run [green][bold]fob gm[/green][/bold] to start a new day.")
        return


    if args.debug:
        print("Buffer entry:")
        pprint(buffer_entry)

    buffer_blocks_left = buffer_entry['allocated'] - buffer_entry['completed']

    if buffer_blocks_left <= 0:
        print("[red][bold]No Buffer blocks left this month.[/red][/bold], so you can't convert any more blocks to Buffer blocks.")
        print("Consider running [green]fob new_month[/green] if you want to reset the block allocations for this month.")
        return

    # guard for: there are blocks assigned to this day (it could be that right before the first day of the month, the checklist is empty.)
    if len(data['checklist']) == 0:
        print("[red][bold]Error: No blocks assigned to today[/red][/bold]. Run [green]fob gm[/green] to assign blocks to today.")
        return

    # ask user which number they want to convert to buffer block
    try:
        # num_to_convert = int(Prompt.ask("Which number would you like to convert to a Buffer block?", default="1"))
        num_to_convert = int(args.block_id)
        # validate input to be between 1 and number of blocks today
        num_blocks_today = len(data['checklist'])
        if num_to_convert < 1 or num_to_convert > num_blocks_today:
            print("[red][bold]Please enter a number that corresponds to the checklist item[/red][/bold]")

        # fetch area name for that number
        # convert index back to string because keys in db are string
        area_to_decrement = data['checklist'][str(num_to_convert)]['name']

        if area_to_decrement == 'Buffer':
            print("[red][bold]Error: This block is already a Buffer block.[/red][/bold]")
            return

        if args.debug:
            print("Field to decrement:")
            print(area_to_decrement)

        # first, modify checklist
        data['checklist'][str(num_to_convert)]['name'] = "Buffer"
        data['checklist'][str(num_to_convert)]['done'] = True

        # second, modify area assignments
        data['areas']['Buffer']['completed'] += 1
        data['areas'][area_to_decrement]['completed'] -= 1

        q = Query()
        db.update({"areas": data['areas']}, q.year == today.year and q.month == today.month)
        db.update({"checklist": data['checklist']}, None)

        # print success message
        display_checklist(args, db)
        print(f"[green]Block {num_to_convert} converted to Buffer block.[/green] See overview: [green]fob sup[/green]")

    except ValueError:
        print("[red][bold]Please enter a number that corresponds to the checklist item[/red][/bold]")
    except KeyError:
        print("[red][bold]Program Error: Database seems to be malformed.[/red][/bold] Please report this issue. In the meantime, consider [green]fob reset[/green] to delete the database and start fresh.")
        return
