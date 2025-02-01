from argparse import Namespace

from rich import print

from fob.db.wrapper import TinyDBWrapper
from fob.utils import get_db_path
from fob.utils import get_version_number

def info(args: Namespace, db: TinyDBWrapper):
    '''
    Display basic metadata about this program.
    '''
    version_number = ".".join(map(str, get_version_number()))
    print("[reverse] Program Information [/reverse]")
    print(f"[bold]fob[/bold] version {version_number} - Simple monthly time management CLI tool.")
    print("Created by tensorturtle https://www.github.com/tensorturtle")
    print("Licensed under the MIT License. https://opensource.org/license/mit")
    print("\n")
    print("[reverse] Configuration Information [/reverse]")
    print(f"Using database at: [magenta]{get_db_path(args)}[/magenta]")