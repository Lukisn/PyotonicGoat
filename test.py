#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tester."""

from datetime import datetime
from io import StringIO
from os.path import isdir
import unittest


class Tester:
    """Tester."""

    ERROR = "ERROR"  # an error occurred during the test
    FAILURE = "FAILURE"  # the test failed
    ISSUES = "ISSUES"  # the test contains issues (e.g. unexpected success)
    SUCCESS = "SUCCESS"  # the test ran successfully
    NEUTRAL = "NEUTRAL"  # no tests or some other neutral state

    def __init__(self, base):
        """Initializer."""
        if not isdir(base):
            raise IOError("Base dir '{}' does not exist!".format(base))
        self.base = base
        self.last_result = None
        self.last_time = None
        self.test()

    def test(self):
        """Run unit tests with automatic discovery and save results."""
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=self.base)
        runner = unittest.TextTestRunner(stream=StringIO(), verbosity=2)
        result = runner.run(suite)
        self.last_time = datetime.now()
        self.last_result = result

    def status(self):
        """Return the status of the last test."""
        if self.last_result.testsRun == 0:
            return self.NEUTRAL
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

    def successful(self):
        run = self.last_result.testsRun
        errors = len(self.last_result.errors)
        failures = len(self.last_result.failures)
        unexpected = len(self.last_result.unexpectedSuccesses)
        unsuccessful = errors + failures + unexpected
        successful = run - unsuccessful
        return successful


if __name__ == "__main__":
    tester = Tester(base=".")
    tester.test()
    print(tester.status())
