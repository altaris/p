"""
This module provides functionality for setting up and managing logging using
[loguru](https://loguru.readthedocs.io/en/stable/overview.html). It includes a
function to configure logging levels and formats.

Note that in this codebase, loguru's logging object is imported as

```py
from loguru import logger as logging
```
"""

import os
import sys
from logging import _nameToLevel
from typing import Any

from loguru import logger as logging


def _is_rank_zero() -> bool:
    """
    Check if the current process is rank 0 in distributed training.

    Returns:
        True if rank 0 or not in distributed mode, False otherwise.
    """
    try:
        import torch.distributed as dist

        if dist.is_available() and dist.is_initialized():
            return dist.get_rank() == 0
    except (ImportError, AttributeError):
        pass
    for env_var in ["LOCAL_RANK", "RANK"]:
        rank_str = os.getenv(env_var)
        if rank_str is not None:
            try:
                rank = int(rank_str)
                return rank == 0
            except ValueError:
                pass
    return True


LOGGING_LEVELS: list[str] = sorted(list(_nameToLevel.keys()))
"""Allowed logging levels (up to case insensitivity)"""


def setup_logging(
    logging_level: str | None = None,
    use_tqdm: bool = True,
    context: dict[str, Any] | None = None,
    **kwargs: Any,
) -> None:
    """
    Sets logging format and level. The format is

        %(asctime)s [%(levelname)-8s] %(message)s

    e.g.

        2022-02-01 10:41:43,797 [INFO    ] Hello world
        2022-02-01 10:42:12,488 [CRITICAL] We're out of beans!

    if there is a context say `context = {"job_id": 3, "weather": "sunny"}`, the
    format changes to

        %(asctime)s [%(levelname)-8s] (job_id=3 weather=sunny) %(message)s

    Args:
        logging_level (str | None): Logging level in `LOGGING_LEVELS` (case
            insensitive, e.g., 'INFO', 'DEBUG', 'WARNING'). If None, reads from
            environment variable `LOGGING_LEVEL`, defaulting to "info".
        use_tqdm (bool): Whether to use `tqdm.write` for logging output to
            avoid conflicts with progress bars. See the loguru-tqdm recipe:
            https://loguru.readthedocs.io/en/stable/resources/recipes.html#interoperability-with-tqdm-iterations
            If tqdm is not installed, silently falls back to sys.stderr.
        **kwargs: Additional keyword arguments passed to
        [`loguru.Logger.add`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add).

    Raises:
        ValueError: If the provided logging level is not valid.
    """

    if not logging_level:
        logging_level = os.getenv("LOGGING_LEVEL", "info")
    assert isinstance(logging_level, str)  # for typechecking
    logging_level = logging_level.upper()
    if logging_level not in LOGGING_LEVELS:
        raise ValueError(
            "Logging level must be one of "
            + ", ".join(map(lambda s: f"'{s}'", LOGGING_LEVELS))
            + " (case insensitive)"
        )

    kw = {
        "enqueue": True,
        "colorize": True,
        "backtrace": True,
        "diagnose": True,
        "filter": lambda _: _is_rank_zero(),
    }
    kw.update(kwargs)

    context_str = ""
    if context:
        context_items = [f"{k}={v}" for k, v in context.items()]
        context_str = " ".join(context_items)
        context_str = f"<cyan>({context_str})</cyan> "

    sink = sys.stderr
    if use_tqdm:
        try:
            from tqdm.auto import tqdm

            sink = lambda msg: tqdm.write(msg, end="")
        except ImportError:
            pass

    logging.remove()
    logging.add(
        sink=sink,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
            + "[<level>{level: <8}</level>] "
            + context_str
            + "<level>{message}</level>"
        ),
        level=_nameToLevel[logging_level],
        **kw,
    )  # type: ignore
