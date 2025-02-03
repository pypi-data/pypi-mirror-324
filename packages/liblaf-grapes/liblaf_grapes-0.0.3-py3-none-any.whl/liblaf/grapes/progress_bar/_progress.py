from rich.console import Console, RenderableType
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Column
from rich.text import Text

from liblaf import grapes


class RateColumn(ProgressColumn):
    unit: str = "it"

    def __init__(self, unit: str = "it", table_column: Column | None = None) -> None:
        super().__init__(table_column)
        self.unit = unit

    def render(self, task: Task) -> RenderableType:
        if not task.speed:
            return Text(f"?{self.unit}/s", style="progress.data.speed")
        human: str = grapes.human_throughout(task.speed, self.unit)
        return Text(human, style="progress.data.speed")


def progress(
    *columns: str | ProgressColumn, console: Console | None = None
) -> Progress:
    if not columns:
        columns: list[ProgressColumn] = [SpinnerColumn()]
        columns.append(TextColumn("[progress.description]{task.description}"))
        columns += [
            BarColumn(),
            TaskProgressColumn(show_speed=True),
            MofNCompleteColumn(),
            "[",
            TimeElapsedColumn(),
            "<",
            TimeRemainingColumn(),
            ",",
            RateColumn(),
            "]",
        ]
    if not console:
        console = grapes.logging_console()
    progress = Progress(*columns, console=console)
    return progress
