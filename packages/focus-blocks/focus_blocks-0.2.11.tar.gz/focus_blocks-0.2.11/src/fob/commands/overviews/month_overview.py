from argparse import Namespace
from datetime import date
from calendar import monthrange

from tinydb import where
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TaskProgressColumn, TextColumn, ProgressColumn
from rich.rule import Rule
from rich.text import Text
from rich import print

from fob.db import TinyDBWrapper

# Custom Column to display assigned / total values
class RawQuantityColumn(ProgressColumn):
    def render(self, task) -> Text:
        completed_total = f"{task.completed:.0f} / {task.total:.0f}"
        return Text(completed_total, style="progress.data")

def month_overview(args: Namespace, db: TinyDBWrapper) -> None:
    today = date.today()
    try:
        data = db.search(where('year') == today.year and where('month') == today.month)[0]
    except IndexError:
        print("[red][bold]No month data found.[/red][/bold]")
        print("Run [green][bold]fob new_month[/green][/bold] to start a new month.")
        return

    console = Console()

    m_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        RawQuantityColumn(),
        disable=True
    )

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        RawQuantityColumn(),
        disable=True
    )

    days_in_month = monthrange(today.year, today.month)[1]

    with m_progress:
        task = m_progress.add_task("Month", total=days_in_month)
        m_progress.update(task, completed=today.day)

        task = m_progress.add_task("Work Days", total=data['work_days_allocated'])
        m_progress.update(task, completed=data['work_days_completed'])

    with progress:
        for area_name, blocks in data['areas'].items():
            task = progress.add_task(f"[bold]{area_name}[/bold]", total=blocks['allocated'])
            progress.update(task, completed=blocks['completed'])

    panel = Panel(Group(m_progress, Rule(style='cyan'), progress), title="This Month", border_style="bold cyan")
    console.print(panel)
