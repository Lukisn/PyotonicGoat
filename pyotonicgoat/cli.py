#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import os
import subprocess
import sys
import tempfile
import time
from argparse import ArgumentParser

from pyotonicgoat.scanning import Scanner
from pyotonicgoat.testing import ResultAdapter
from pyotonicgoat.util import now, colored, colored_status


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = ArgumentParser("Run PyotonicGoat CLI")
    parser.add_argument(
        "base", type=str,
        help="Base directory to scan and run tests from")
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="scan interval in seconds")
    args = parser.parse_args(argv)
    return args


class GoatCLI:
    """Pyotonic Goat Command Line Interface."""

    def __init__(self, base):
        """Initializer."""
        self.indicator = itertools.cycle("|/-\\")
        self.last_result = None
        self.bleat("starting up ...")
        self.scanner = Scanner(base=base)
        self.tmp = tempfile.TemporaryDirectory()
        self.file = os.path.join(self.tmp.name, "results.json")
        self.test()

    def trigger(self):
        """Trigger a check if the scanned directory has changed."""
        self.bleat("scanning")
        if self.scanner.has_changed():
            self.bleat("testing")
            self.test()
            self.bleat("done")
            self.scanner.scan()

    def test(self):
        """Run a testing session"""
        subprocess.run(["python3", "testing.py", self.scanner.base, "-o", self.file])
        result = ResultAdapter.from_json(self.file)
        self.last_result = result
        return result

    def bleat(self, msg):
        """Output information to the command line."""
        # fmt = "[{time}] {ind} [{status:^7s}] {green}/{run} {info}- {msg}"
        fmt = "\r[{time}] {ind} [{status:^7s}] {green}/{run} {info}- {msg}"
        time_fmt = "%H:%M:%S"
        info = ""
        if self.last_result is None:
            status = "?"
            green = "~*~"
            run = "~*~"
        else:
            status = self.last_result.status()
            green = self.last_result.successful_tests()
            run = self.last_result.testsRun

            errors = len(self.last_result.errors)
            failures = len(self.last_result.failures)
            skipped = len(self.last_result.skipped)
            expected = len(self.last_result.expectedFailures)
            unexpected = len(self.last_result.unexpectedSuccesses)

            infos = []
            if errors > 0:
                error_info = colored("{} err ".format(errors), "yellow")
                infos.append(error_info)
            if failures > 0:
                failure_info = colored("{} fail ".format(failures), "red")
                infos.append(failure_info)
            if unexpected > 0:  # unexpected Successes are failures too!
                unexpected_info = colored(
                    "{} unexpected success".format(unexpected),
                    "red")
                infos.append(unexpected_info)
            if skipped > 0:
                skipped_info = "{} skip ".format(skipped)
                infos.append(skipped_info)
            if expected > 0:
                expected_info = "{} xfail ".format(expected)
                infos.append(expected_info)
            if info:
                info = "({}) ".format(" ".join(infos))

        print(fmt.format(time=now().strftime(time_fmt),
                         status=colored_status(status),
                         green=green, run=run, info=info, msg=msg,
                         ind=next(self.indicator)),
              end="", flush=True)


def main():
    args = parse_args()
    cli = GoatCLI(base=args.base)
    while True:
        cli.trigger()
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
