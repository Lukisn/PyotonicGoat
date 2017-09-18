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


def main():
    args = parse_args()
    print(args)

    scanner = Scanner(base=args.base)
    tester = Tester(base=args.base)
    print(tester.last_result)

    while True:
        if scanner.has_changed():
            print(scanner.last_time)
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
