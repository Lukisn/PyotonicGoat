#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`test` module."""

from datetime import datetime
from os.path import abspath, dirname, exists, join
import unittest
# tester

HERE = dirname(abspath(__file__))


class ExampleTestCase(unittest.TestCase):

    def test_success(self):
        pass

    def test_failure(self):
        self.fail()

    def test_error(self):
        raise RuntimeError("Unexpected Error")

    @unittest.skip("test skipping")
    def test_skipped(self):
        pass

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.fail()

    @unittest.expectedFailure
    def test_unexpected_success(self):
        pass


class TestTesterInitialization(unittest.TestCase):
    """Unit test case for ``Tester`` initialization."""

    pass


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
