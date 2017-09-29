#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility module."""

from datetime import datetime, timezone


def now():
    """Get a timezone aware local current datetime object."""
    return datetime.now(timezone.utc).astimezone()


def colored(text, color, bold=False, bg_color="default"):
    """Return colored text for output on the terminal."""
    color_codes = {
        "default": 0, "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37}
    bg_color_codes = {
        "default": 0, "black": 40, "red": 41, "green": 42, "yellow": 43,
        "blue": "44", "magenta": 45, "cyan": 46, "white": 47}
    color_code = color_codes.get(color, "default")
    bg_color_code = bg_color_codes.get(bg_color, "default")
    bold_code = "1" if bold else "0"
    modifier = f"\033[{color_code};{bold_code};{bg_color_code}m"
    reset = "\033[0;0;0m"
    return f"{modifier}{text}{reset}"


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
