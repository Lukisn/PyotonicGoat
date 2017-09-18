#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import time
from scan import Scanner
from test import Tester


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base", help="Base directory to scan and run tests from")
    args = parser.parse_args(argv)
    return args


def print_status_line(time="-", status="?", failed="-", run="-", action="."):
    fmt = "\r[{time}] {status} {failed}/{run} {action}"

    print(fmt.format(time=time, status=status, failed=failed, run=run,
                     action=action),
          end="", flush=True)


def main():
    args = parse_args()
    print(args)

    scanner = Scanner(base=args.base)
    tester = Tester(base=args.base)
    print(tester.last_result)

    while True:
        # print_status_line(action="scanning...")
        if scanner.has_changed():
            # print_status_line("testing...")
            tester.test()
            print_status_line(tester.last_time, "OK?", "x", "y")
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
