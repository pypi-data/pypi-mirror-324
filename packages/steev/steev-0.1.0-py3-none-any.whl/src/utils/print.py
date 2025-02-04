import sys
import time
from typing import Optional, Literal

import click


def print_line(
    new_line_direction: Literal["up", "down", "both", "none"],
    line_length: int = 40,
) -> None:
    if new_line_direction == "both":
        click.echo("\n" + "─" * line_length + "\n")
    elif new_line_direction == "up":
        click.echo("\n" + "─" * line_length)
    elif new_line_direction == "down":
        click.echo("─" * line_length + "\n")


def typing_print(
    text: str, delay: float = 0.01, color: Optional[str] = None, keywords: Optional[list[str]] = None
) -> None:
    if delay > 0:
        if keywords:
            for keyword in keywords:
                text = text.replace(keyword, click.style(keyword, fg=color))
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
            sys.stdout.write("\n")
    else:
        click.echo(click.style(text, fg=color), err=True)


def typing_prompt(
    text: str,
    default: Optional[str] = None,
    type=None,
    delay: float = 0.01,
    color: Optional[str] = None,
    keywords: Optional[list[str]] = None,
) -> str:
    # First display the prompt text with typing effect
    if keywords:
        for keyword in keywords:
            text = text.replace(keyword, click.style(keyword, fg=color))

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    # Modify the default value display format
    if default is not None:
        default_display = f"[{default.upper()}/n]" if default.lower() == "y" else "[y/N]"
        sys.stdout.write(f" {default_display}")

    sys.stdout.write(": ")  # Add the prompt colon
    sys.stdout.flush()

    # Get user input and validate
    while True:
        value = input()
        if not value and default is not None:
            return default
        if type == click.Choice(["y", "n"]):
            value = value.lower()
            if value in ["y", "n"]:
                return value
            click.echo("Please enter 'y' or 'n'")
            continue
        return value
