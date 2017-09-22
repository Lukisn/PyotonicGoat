#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, timezone
import sys
import time
from pyotonicgoat.scanning import Scanner
# tester


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
    args = parser.parse_args(argv)
    return args


def main():
    """Main program."""
    args = parse_args()
    scanner = Scanner(base=args.base)

    while True:
        print("[{}] scanning...".format(now()))
        if scanner.has_changed():
            print("[{}] CHANGED! testing...".format(now()))
            # tester
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
