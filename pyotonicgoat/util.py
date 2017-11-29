#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility module."""

from datetime import datetime, timezone


def now():
    """Get a timezone aware local current datetime object."""
    return datetime.now(timezone.utc).astimezone()


def colored(text, color, background="default", bold=False):
    """Return colored text for output on the terminal."""
    color_codes = {
        "default": 0, "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37}
    background_codes = {
        "default": 0, "black": 40, "red": 41, "green": 42, "yellow": 43,
        "blue": "44", "magenta": 45, "cyan": 46, "white": 47}
    color = color_codes.get(color, "default")
    background = background_codes.get(background, "default")
    bold = 1 if bold else 0
    if not color and not background and not bold:
        return text
    else:
        modifiers = []
        if color:
            modifiers.append(f"\033[{color}m")
        if background:
            modifiers.append(f"\033[{background}m")
        if bold:
            modifiers.append(f"\033[{bold}m")
        modifier = "".join(modifiers)
        reset = "\033[0m"
        return f"{modifier}{text}{reset}"


def bold(text):
    """Return bold text in default color."""
    return colored(text, color="default", background="default", bold=True)


def colored_status(status):
    """Return colored Status text according to status."""
    if status == "Success":
        return colored(status, "green", bold=True)
    elif status == "Error":
        return colored(status, "yellow", bold=True)
    elif status == "Failure":
        return colored(status, "red", bold=True)
    else:
        return status
