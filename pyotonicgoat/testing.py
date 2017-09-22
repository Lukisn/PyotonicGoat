#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tester for running unittests from the command line."""

import argparse
from io import StringIO
import json
import sys
import unittest


class ResultAdapter:
    """Adapter class covering basic information from unittest TestResults."""

    def __init__(self, testsRun, errors, failures, skipped, expectedFailures,
                 unexpectedSuccesses):
        """Initializer."""
        self.testsRun = testsRun  # int
        self.errors = errors  # [(case, traceback), ...]
        self.failures = failures  # [(case, traceback), ...]
        self.skipped = skipped  # [(case, traceback), ...]
        self.expectedFailures = expectedFailures  # [(case, traceback), ...]
        self.unexpectedSuccesses = unexpectedSuccesses  # [case, ...]

    def __repr__(self):
        """Debugging string representation."""
        fmt = ("<{} run={} errors={} failures={} skipped={} "
               "expecteFailures={} unexpectedSuccesses={}>")
        return fmt.format(
            self.__class__.__name__, self.testsRun, len(self.errors),
            len(self.failures), len(self.skipped),len(self.expectedFailures),
            len(self.unexpectedSuccesses))

    @classmethod
    def from_unittest(cls, result):
        """Instantiate object from unittest TestResult."""
        testsRun = result.testsRun
        errors = cls._extract_tuple(result.errors)
        failures = cls._extract_tuple(result.failures)
        skipped = cls._extract_tuple(result.skipped)
        expectedFailures = cls._extract_tuple(result.expectedFailures)
        unexpectedSuccesses = cls._extract(result.unexpectedSuccesses)
        return cls(testsRun, errors, failures, skipped, expectedFailures,
                   unexpectedSuccesses)

    @classmethod
    def from_json(cls, infilename):
        """Instantiate object from a json file."""
        with open(infilename, mode="rt") as infile:
            data = json.load(infile)
        return cls(data["testsRun"], data["errors"], data["failures"],
                   data["skipped"], data["expectedFailures"],
                   data["unexpectedSuccesses"])

    def write_json(self, outfilename):
        """Dump the object into a json file."""
        data = {
            "testsRun": self.testsRun,
            "errors": self.errors,
            "failures": self.failures,
            "skipped": self.skipped,
            "expectedFailures": self.expectedFailures,
            "unexpectedSuccesses": self.unexpectedSuccesses
        }
        with open(outfilename, mode="wt") as outfile:
            json.dump(data, outfile, indent=4)

    @staticmethod
    def _qualified_name(case):
        """Build the fully qualified name of a unittest test method."""
        return "{}.{}.{}".format(case.__class__.__module__,
                                 case.__class__.__qualname__,
                                 case._testMethodName)

    @staticmethod
    def _extract_tuple(test_list):
        """Extract test method names and tracebacks from a list of 2-tuples."""
        test_dict = {}
        for case, traceback in test_list:
            name = ResultAdapter._qualified_name(case)
            test_dict[name] = traceback
        return test_dict

    @staticmethod
    def _extract(test_list):
        """Extract test method names from a list of unittest TestCases."""
        list = []
        for case in test_list:
            name = ResultAdapter._qualified_name(case)
            list.append(name)
        return list

    def successful_tests(self):
        """Get the number of successful tests."""
        successful = self.testsRun
        successful -= len(self.errors)
        successful -= len(self.failures)
        successful -= len(self.unexpectedSuccesses)
        return successful

    def status(self):
        """Get the overall status of the test result."""
        if len(self.errors):
            return "ERROR"
        elif len(self.failures) or len(self.unexpectedSuccesses):
            return "FAILURE"
        else:
            return "SUCCESS"


def run_tests(base):
    """Run unittests by automatic discovery in the given base directory."""
    suite = unittest.defaultTestLoader.discover(base)
    runner = unittest.TextTestRunner(stream=StringIO(), verbosity=2)
    result = runner.run(suite)
    return result


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base", type=str,
        help="Base directory to run tests from")
    parser.add_argument(
        "-o", "--output", type=str, default="results.json",
        help="Output file for storing the test results")
    args = parser.parse_args(argv)
    return args


def main():
    """Main program."""
    args = parse_args()
    result = run_tests(args.base)
    # print(result)
    # print(result.errors[0])
    # print(result.errors[0][0].__dict__)
    adapted_result = ResultAdapter.from_unittest(result)
    # print(adapted_result)
    adapted_result.write_json(args.output)
    # reread_result = adapted_result.from_json("outfile.json")
    # print(reread_result)


if __name__ == "__main__":
    sys.exit(main())
