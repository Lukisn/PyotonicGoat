#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, timezone
import subprocess
import sys
import time
from pyotonicgoat.scanning import Scanner
from pyotonicgoat.testing import ResultAdapter


def now():
    """Get a timezone aware local current timestamp."""
    return datetime.now(timezone.utc).astimezone()


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base", type=str,
        help="Base directory to scan and run tests from")
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="scan interval in seconds")
    parser.add_argument(
        "-f", "--file", type=str, default="results.json",
        help="Intermediate result file name"
    )
    args = parser.parse_args(argv)
    return args


def run_tests_in_subprocess(args):
    """Run unittests in a dedicated subprocess."""
    subprocess.run(["python3", "testing.py", args.base, "-o", args.file])
    return ResultAdapter.from_json(args.file)


# TODO: unify printing -> CLI class ?
def print_message(message):
    fmt = "\r[{time}] - {msg}"
    time_fmt = "%H:%M:%S"
    print(fmt.format(time=now().strftime(time_fmt), msg=message),
          end="", flush=True)


def print_status(result, message, color=None, status=None):
    """Print status line to the command line."""
    fmt = "\r[{time}] [{color}{status:^7s}{reset}] {succ} / {run} - {msg}"
    time_fmt = "%H:%M:%S"
    colors = {
        "ERROR": "\033[33;1m",  # yellow
        "FAILURE": "\033[31;1m",  # red
        "SUCCESS": "\033[32;1m",  # green
        "NEUTRAL": "\033[34;1m",  # blue
        "RESET": "\033[0m"
    }
    if color is None:
        color = result.status()
    if status is None:
        status = result.status()
    print(fmt.format(time=now().strftime(time_fmt),
                     color=colors[color],
                     status=status,
                     reset=colors["RESET"],
                     succ=result.successful_tests(),
                     run=result.testsRun,
                     msg=message), end="", flush=True)


def main():
    """Main program."""
    args = parse_args()
    print_message("starting up...")
    scanner = Scanner(base=args.base)
    result = run_tests_in_subprocess(args)
    print_status(result, "initial result.")
    scanner.scan()

    while True:
        print_status(result, "scanning...")
        if scanner.has_changed():
            print_status(result, "testing...", color="NEUTRAL", status="?")
            result = run_tests_in_subprocess(args)
            print_status(result, "done.")
            scanner.scan()
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
