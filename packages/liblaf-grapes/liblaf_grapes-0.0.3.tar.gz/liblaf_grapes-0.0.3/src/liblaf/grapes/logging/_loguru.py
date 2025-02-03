import contextlib
import inspect
import itertools
import logging
from collections.abc import Iterable, Sequence

import loguru
from environs import Env
from loguru import logger
from rich.logging import RichHandler

from liblaf import grapes

type Filter = "str | loguru.FilterDict | loguru.FilterFunction"


DEFAULT_FILTER: Filter = {
    "": "INFO",
    "__main__": "TRACE",
    "liblaf": "DEBUG",
}


DEFAULT_LEVELS: Sequence["loguru.LevelConfig"] = [
    {"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}
]


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages toward Loguru sinks.

    References:
        [1] [Overview — loguru documentation](https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging)
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def add_level(
    name: str, no: int, color: str | None = None, icon: str | None = None
) -> None:
    with contextlib.suppress(ValueError):
        logger.level(name, no, color=color, icon=icon)


def setup_loguru_logging_intercept(
    level: int | str = logging.NOTSET, modules: Iterable[str] = ()
) -> None:
    """...

    References:
        [1] [loguru-logging-intercept/loguru_logging_intercept.py at f358b75ef4162ea903bf7a3298c22b1be83110da · MatthewScholefield/loguru-logging-intercept](https://github.com/MatthewScholefield/loguru-logging-intercept/blob/f358b75ef4162ea903bf7a3298c22b1be83110da/loguru_logging_intercept.py#L35C5-L42)
    """
    logging.basicConfig(level=level, handlers=[InterceptHandler()])
    for logger_name in itertools.chain(("",), modules):
        mod_logger: logging.Logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler(level=level)]
        mod_logger.propagate = False


def init_loguru(
    level: int | str = logging.NOTSET,
    filter: Filter | None = None,  # noqa: A002
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
) -> None:
    filter = filter or DEFAULT_FILTER  # noqa: A001
    if handlers is None:
        handlers: list[loguru.HandlerConfig] = [
            {
                "sink": RichHandler(
                    console=grapes.logging.logging_console(),
                    omit_repeated_times=False,
                    markup=True,
                    log_time_format="[%Y-%m-%d %H:%M:%S]",
                ),
                "format": "{message}",
                "filter": filter,
            }
        ]
        env: Env = grapes.environ.init_env()
        if fpath := env.path("LOGGING_FILE", None):
            handlers.append({"sink": fpath, "filter": filter, "mode": "w"})
        if fpath := env.path("LOGGING_JSONL", None):
            handlers.append(
                {"sink": fpath, "filter": filter, "serialize": True, "mode": "w"}
            )
    logger.configure(handlers=handlers)
    for lvl in levels or DEFAULT_LEVELS:
        add_level(**lvl)
    setup_loguru_logging_intercept(level=level)
