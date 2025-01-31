from datetime import date
from calendar import monthrange
from argparse import Namespace

from rich.prompt import Prompt
from rich import print
from rich.table import Table
from rich.console import Console
from tinydb import where, Query

from fob.db import TinyDBWrapper
from fob.db import MonthBlockData

def new_month(args: Namespace, db: TinyDBWrapper) -> None:
    '''
    Assign blocks to areas for the new month.
    '''
    result = loop_until_user_happy(args)
    if result is not None:
        write_new_month(result, db)
        print("\n[green]New month successfully created![/green]")
        print("Start your day: [green][bold]fob gm[/green][/bold]")

def write_new_month(data: MonthBlockData, db: TinyDBWrapper) -> None:
    areas = {}
    for area, blocks in data.blocks_per_area.items():
        areas[area] = {
            "allocated": blocks,
            "completed": 0,
        }

    # Overwrite the existing month data (shouldn't happen but avoids duplicates)
    q = Query()
    db.upsert({
        "year": data.year,
        "month": data.month,
        "work_days_allocated": data.work_days_allocated,
        "work_days_completed": 0,
        "blocks_per_day": data.blocks_per_day,
        "areas": areas,
    }, q.year == data.year and q.month == data.month)

def loop_until_user_happy(args: Namespace) -> MonthBlockData | None:
    user_is_happy = False
    while not user_is_happy:
        result = converse_with_user(args)
        unallocated_existed, blocks_per_area = distribute_unallocated(result.blocks_per_area)
        display_blocks_table(blocks_per_area, None)

        if (
            Prompt.ask(
                "\nAre you happy with the allocation?",
                choices=["yes", "no"],
                default="no" if unallocated_existed else "yes",
            )
            == "yes"
        ):
            return result

        print("[yellow]Starting over...[/yellow]\n")

def simplify_value_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print(
                "[red bold]Error:[/red bold] It seems you have entered an invalid value. Please try again."
            )

    return wrapper


#@simplify_value_errors
def converse_with_user(args: Namespace) ->MonthBlockData:
    print("New month! Let's allocate blocks for the upcoming month.")
    print(
        "Press [cyan][bold]enter[/cyan][/bold] to accept the [cyan][bold](default value)[/cyan][/bold]."
    )
    today = date.today()
    if today.day > 2:
        print(
            f"Today is {today}. It's probably time to allocate blocks for the next month."
        )
        today = today.replace(day=1)
        # Modulo math to handle December (increment year and return month to 1)
        today = today.replace(year=today.year + ((today.month + 1) // 12))
        today = today.replace(month=(today.month + 1) % 12)
    year = Prompt.ask("\nWhat year?", default=str(today.year))
    month = Prompt.ask("What month?", default=str(today.month))

    days_in_month = monthrange(int(year), int(month))[1]

    if args.debug:
        print(f"\nAllocating blocks for {year}/{month}, which has {days_in_month} days.")

    working_days = Prompt.ask(
        "How many working days?", default=str(days_in_month - 8)
    )
    if int(working_days) > days_in_month or int(working_days) <= 0:
        print(
            "[red bold]Error:[/red bold] Invalid number of working days. Please try again."
        )

    if args.debug:
        print(f"You have chosen {working_days} working days.")

    blocks_per_day = Prompt.ask("How many blocks per day?", default="5")
    total_blocks = int(working_days) * int(blocks_per_day)
    print("---")
    print(
        f"You have chosen {blocks_per_day} blocks per day, for a total of {total_blocks} blocks.\n"
    )

    print("Which areas will you be working on?")
    areas = []

    while True:
        area = Prompt.ask("New Focus Area (enter empty to finish)", default="")
        if area == "":
            break
        areas.append(area)

    if args.debug:
        print(f"You have chosen the following areas: {', '.join(areas)}")

    blocks_per_area = {}
    for area in areas:
        blocks_per_area[area] = 0

    areas.append("Buffer")
    default_buffer = min(8, total_blocks)
    buffer_blocks = Prompt.ask(
        "How many blocks for Buffer?", default=str(default_buffer)
    )
    blocks_per_area.update({"Buffer": int(buffer_blocks)})

    for i, area in enumerate(areas):
        if i == len(areas) - 1:
            # Don't count buffer
            break
        remaining_blocks = total_blocks - sum(blocks_per_area.values())
        if args.debug:
            print(f"You have {remaining_blocks} blocks remaining.")
        display_blocks_table(blocks_per_area, area)
        equal_split_from_remaining = remaining_blocks // (len(areas) - i - 1)
        blocks_for_area = int(
            Prompt.ask(
                f"How many blocks for {area}?",
                default=str(equal_split_from_remaining),
            )
        )
        if blocks_for_area < 0 or blocks_for_area > remaining_blocks:
            raise ValueError("Invalid value")
        blocks_per_area[area] = blocks_for_area
        print("\n")

    blocks_per_area.update(
        {"Unallocated": total_blocks - sum(blocks_per_area.values())}
    )

    display_blocks_table(blocks_per_area, None)

    return MonthBlockData(
        year=int(year),
        month=int(month),
        work_days_allocated=int(working_days),
        blocks_per_day=int(blocks_per_day),
        blocks_per_area=blocks_per_area,
    )

def distribute_unallocated(blocks_per_area) -> tuple[bool, dict[str, int]]:
    """
    Returns (bool, dict[str, int]) where
    bool is True if unallocated blocks exist and this function actually modifies the dictionary, False otherwise
    """
    unallocated = blocks_per_area.pop("Unallocated")
    exists_unallocated = unallocated > 0
    if exists_unallocated:
        print(
            "\n[yellow][bold]Unallocated blocks detected.[/bold] Distributing them evenly among the focus areas...[/yellow]\n"
        )
        try:
            add_to_each = unallocated // (len(blocks_per_area) - 1)
        except ZeroDivisionError:
            add_to_each = 0
        for area, blocks in blocks_per_area.items():
            if area != "Buffer":
                blocks_per_area[area] = blocks + add_to_each
                unallocated -= add_to_each

        # remainder (from whole division) goes to buffer
        blocks_per_area["Buffer"] += unallocated

    return (exists_unallocated, blocks_per_area)


def display_blocks_table(blocks: dict[str, int], highlight: str | None) -> None:
    """
    Table view of the month's blocks allocation per focus area.
    """
    table = Table(title="Month's Blocks Allocation")
    for area in blocks.keys():
        table.add_column(area, justify="center", style="magenta")

    # highlight the focus area
    table.add_row(
        *[
            str(blocks[area]) if area != highlight else f"[reverse]{blocks[area]}[/reverse]"
            for area in blocks.keys()
        ]
    )

    console = Console()
    console.print(table)
