#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tester."""

import datetime
from io import StringIO
from os.path import isdir
import unittest


class Tester:
    """Tester."""

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

    # TODO: results extraction
    def status(self):
        """Return the status of the last test."""
        print(self.last_result.__dict__)
        print(self.last_result.testsRun)
        print(self.last_result.errors)
        print(self.last_result.failures)
        print(self.last_result.skipped)
        print(self.last_result.expectedFailures)
        print(self.last_result.unexpectedSuccesses)



if __name__ == "__main__":
    tester = Tester(base=".")
    tester.test()
    tester.status()
