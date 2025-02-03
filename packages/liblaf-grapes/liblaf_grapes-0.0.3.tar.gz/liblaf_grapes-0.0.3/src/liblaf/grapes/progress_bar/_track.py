from collections.abc import Generator, Iterable
from typing import Any, TypeVar

from rich.progress import Progress

from liblaf import grapes

from . import progress

_T = TypeVar("_T")


def track(
    sequence: Iterable[_T],
    *,
    description: str | bool | None = True,
    record_log_level: int | str | None = "DEBUG",
    report_log_level: int | str | None = "INFO",
    timer: bool = True,
    total: float | None = None,
) -> Generator[_T, Any, None]:
    if description is True:
        description = grapes.caller_location(2)
    description = description or ""
    prog: Progress = progress()
    if timer:
        t = grapes.timer(
            label=description,
            report_at_exit=False,
            record_log_level=record_log_level,
            report_log_level=report_log_level,
        )
        with prog:
            yield from t.track(
                prog.track(sequence, total=total, description=description)
            )
            t.log_report()
    else:
        with prog:
            yield from prog.track(sequence, description=description)
