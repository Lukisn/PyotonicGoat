#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import time
from scan import Scanner
from test import Tester
# TODO: check why updates keep untested


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base", type=str,
        help="Base directory to scan and run tests from"
    )
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="scan interval in seconds"
    )
    args = parser.parse_args(argv)
    return args


def print_status_line(tester):
    """Print a line about the last test runs status to the terminal."""
    time_fmt = "%H:%M:%S"
    main_fmt = "[{time}] [{status:7s}] {successful} / {tests_run}"
    print(main_fmt.format(
        time=tester.last_time.strftime(time_fmt),
        status=tester.status(),
        successful=tester.successful(),
        tests_run=tester.last_result.testsRun,
    ))


def main():
    """Main program."""
    args = parse_args()
    scanner = Scanner(base=args.base)
    tester = Tester(base=args.base)
    print_status_line(tester)

    while True:
        if scanner.has_changed():
            tester.test()
            print_status_line(tester)
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
