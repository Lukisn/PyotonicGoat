#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tester module.

This module contains the tester class and acts as an executable command line
script for running the tests in a subprocess.
"""

from argparse import ArgumentParser
from io import StringIO
from json import load, dump
from os.path import isdir, join
from subprocess import run
from sys import exit
from tempfile import TemporaryDirectory
from unittest import defaultTestLoader, TextTestRunner
from pyotonicgoat.util import now


class ResultAdapter:
    """Adapter containing basic information of test results."""

    def __init__(self, run, errors, failures, skipped, expected, unexpected):
        """Initializer."""
        self.testsRun = run  # int
        self.errors = errors  # [(case, traceback), ...]
        self.failures = failures  # [(case, traceback), ...]
        self.skipped = skipped  # [(case, traceback), ...]
        self.expected = expected  # [(case, traceback), ...]
        self.unexpected = unexpected  # [case, ...]

    def __repr__(self):  # pragma: no cover
        """Debugging string representation."""
        fmt = ("<{} run={} errors={} failures={} skipped={} "
               "expecteFailures={} unexpectedSuccesses={}>")
        return fmt.format(
            self.__class__.__name__, self.testsRun, len(self.errors),
            len(self.failures), len(self.skipped), len(self.expected),
            len(self.unexpected))

    @classmethod
    def from_unittest(cls, result):
        """Instantiate object from unittest TestResult."""
        testsRun = result.testsRun
        errors = cls._extract_tuple(result.errors)
        failures = cls._extract_tuple(result.failures)
        skipped = cls._extract_tuple(result.skipped)
        expected = cls._extract_tuple(result.expectedFailures)
        unexpected = cls._extract(result.unexpectedSuccesses)
        return cls(testsRun, errors, failures, skipped, expected, unexpected)

    @classmethod
    def from_json(cls, infilename):
        """Instantiate object from a json file."""
        with open(infilename, mode="rt") as infile:
            data = load(infile)
        return cls(data["testsRun"], data["errors"], data["failures"],
                   data["skipped"], data["expected"], data["unexpected"])

    def write_json(self, outfilename):
        """Dump the object into a json file."""
        data = {
            "testsRun": self.testsRun,
            "errors": self.errors,
            "failures": self.failures,
            "skipped": self.skipped,
            "expected": self.expected,
            "unexpected": self.unexpected
        }
        with open(outfilename, mode="wt") as outfile:
            dump(data, outfile, indent=4)

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

    def green(self):
        """Get the number of successful tests."""
        successful = self.testsRun
        successful -= len(self.errors)
        successful -= len(self.failures)
        successful -= len(self.unexpected)
        return successful

    def status(self):
        """Get the overall status of the test result."""
        if len(self.errors):
            return "Error"
        elif len(self.failures) or len(self.unexpected):
            return "Failure"
        else:
            return "Success"


class Tester:
    """Simple unittest runner."""

    def __init__(self, base):
        """Initializer."""
        if not isdir(base):
            raise IOError("Base dir '{}' does not exist!".format(base))
        self.base = base
        self.tmp_dir = TemporaryDirectory()
        self.file = join(self.tmp_dir.name, "results.json")
        self.last_time = None
        self.last_result = None
        self.test()  # initialize tester with first test result

    def __del__(self):
        """'Destructor'."""
        self.tmp_dir.cleanup()

    def test(self):
        """Run the unittests in a dedicated subprocess."""
        run(["python3", __file__, self.base, "-o", self.file])
        result = ResultAdapter.from_json(self.file)

        self.last_time = now()
        self.last_result = result
        return result


def run_tests(base):
    """Run unittests by automatic discovery in the given base directory."""
    suite = defaultTestLoader.discover(base)
    runner = TextTestRunner(stream=StringIO(), verbosity=2)
    result = runner.run(suite)
    return result


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = ArgumentParser()
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
    adapted_result = ResultAdapter.from_unittest(result)
    adapted_result.write_json(args.output)


if __name__ == "__main__":
    exit(main())
