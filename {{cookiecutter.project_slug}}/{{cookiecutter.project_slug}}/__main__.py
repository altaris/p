"""
Entry point
"""
__docformat__ = "google"


import logging
import os

{% if cookiecutter.click_main == "y" %}
import click

{% endif %}
def _setup_logging(logging_level: str) -> None:
    """
    Sets logging format and level. The format is

        %(asctime)s [%(levelname)-8s] %(message)s

    e.g.

        2022-02-01 10:41:43,797 [INFO    ] Hello world
        2022-02-01 10:42:12,488 [CRITICAL] We're out of beans!

    Args:
        logging_level (str): Either 'critical', 'debug', 'error', 'info', or
            'warning', case insensitive. If invalid, defaults to 'info'.
    """
    logging_levels = {
        "critical": logging.CRITICAL,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "info": logging.INFO,
        "warning": logging.WARNING,
    }
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        level=logging_levels.get(logging_level.lower(), logging.INFO),
    )

{% if cookiecutter.click_main == "y" %}
@click.command()
@click.option(
    "--logging-level",
    default=os.getenv("LOGGING_LEVEL", "info"),
    help=(
        "Logging level, among 'critical', 'debug', 'error', 'info', and "
        "'warning', case insensitive."
    ),
    type=click.Choice(
        ["critical", "debug", "error", "info", "warning"],
        case_sensitive=False,
    ),
)
def main(
    logging_level: str,
):
    """Entrypoint."""
    _setup_logging(logging_level)
{% else %}
def main():
    """Entrypoint."""
    _setup_logging(os.getenv("LOGGING_LEVEL", "info"))
{% endif %}

# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
