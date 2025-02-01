from dataclasses import dataclass

from fob.db.wrapper import TinyDBWrapper

@dataclass
class MonthBlockData:
    year: int
    month: int
    work_days_allocated: int
    blocks_per_day: int
    blocks_per_area: dict[str, int]


def checklist_complete(db: TinyDBWrapper) -> bool:
    try:
        return all([info['done'] for info in db.all()[0]['checklist'].values()])
    except KeyError: # 'checklist'
        return False
