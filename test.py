#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tester."""

import datetime
from io import StringIO
from os.path import isdir
import unittest


class Tester:
    """Tester."""

    ERROR = "ERROR"  # an error occurred during the test
    FAILURE = "FAILURE"  # the test failed
    ISSUES = "ISSUES"  # the test contains issues (e.g. unexpected success)
    SUCCESS = "SUCCESS"  # the test ran successfully

    def __init__(self, base):
        """Initializer."""
        if not isdir(base):
            raise IOError("Base dir '{}' does not exist!".format(base))
        self.base = base
        self.last_result = None
        self.last_time = None
        self.last_output = None
        self.test()

    def test(self):
        """Run unit tests with automatic discovery and save results."""
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=self.base)
        output = StringIO()
        runner = unittest.TextTestRunner(stream=output, verbosity=2)
        result = runner.run(suite)
        output.seek(0)
        self.last_time = datetime.datetime.now()
        self.last_result = result
        self.last_output = output.readlines()

    def status(self):
        """Return the status of the last test."""
        errors = self.last_result.errors
        failures = self.last_result.failures
        unexpected_successes = self.last_result.unexpectedSuccesses
        if errors:
            return self.ERROR
        elif failures:
            return self.FAILURE
        elif unexpected_successes:
            return self.ISSUES
        else:
            return self.SUCCESS


if __name__ == "__main__":
    tester = Tester(base=".")
    tester.test()
    print(tester.status())
