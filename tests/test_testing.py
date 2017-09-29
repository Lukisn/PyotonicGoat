#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`test` module."""

from os.path import abspath, dirname
from unittest import TestCase, main
from pyotonicgoat.testing import ResultAdapter
# TODO: find testing strategy and write unit tests


HERE = dirname(abspath(__file__))


class TestTesterInitialization(TestCase):
    """Unit test case for ``Tester`` initialization."""

    def test_empty_default_init(self):
        """Test default initializer initialization with 'empty' values."""
        result = ResultAdapter(
            run=0,
            errors=[],  # [(case, traceback), ...]
            failures=[],  # [(case, traceback), ...]
            skipped=[],  # [(case, traceback), ...]
            expected=[],  # [(case, traceback), ...]
            unexpected=[],  # [case, ...]
        )
        self.assertEqual(0, result.testsRun)
        self.assertIsInstance(result.errors, list)
        self.assertEqual([], result.errors)
        self.assertIsInstance(result.failures, list)
        self.assertEqual([], result.failures)
        self.assertIsInstance(result.skipped, list)
        self.assertEqual([], result.skipped)
        self.assertIsInstance(result.expected, list)
        self.assertEqual([], result.expected)
        self.assertIsInstance(result.unexpected, list)
        self.assertEqual([], result.unexpected)

    def test_default_init(self):
        """Test default initializer with real unit test cases."""
        case = "runTest"
        traceback = "Traceback (most recent call last): ..."
        result = ResultAdapter(
            run=42,
            errors=[(case, traceback)],  # [(case, traceback), ...]
            failures=[(case, traceback)],  # [(case, traceback), ...]
            skipped=[(case, traceback)],  # [(case, traceback), ...]
            expected=[(case, traceback)],  # [(case, traceback), ...]
            unexpected=[case],  # [case, ...]
        )
        self.assertEqual(42, result.testsRun)
        self.assertIsInstance(result.errors, list)
        for error_tuple in result.errors:
            error_case, error_traceback = error_tuple
            self.assertIsInstance(error_case, str)
            self.assertIsInstance(error_traceback, str)
            self.assertEqual(case, error_case)
            self.assertEqual(traceback, error_traceback)
        self.assertIsInstance(result.failures, list)
        for failure_tuple in result.failures:
            failure_case, failure_traceback = failure_tuple
            self.assertIsInstance(failure_case, str)
            self.assertIsInstance(failure_traceback, str)
            self.assertEqual(case, failure_case)
            self.assertEqual(traceback, failure_traceback)
        self.assertIsInstance(result.skipped, list)
        for skipped_tuple in result.skipped:
            skipped_case, skipped_traceback = skipped_tuple
            self.assertIsInstance(skipped_case, str)
            self.assertIsInstance(skipped_traceback, str)
            self.assertEqual(case, skipped_case)
            self.assertEqual(traceback, skipped_traceback)
        self.assertIsInstance(result.expected, list)
        for expected_tuple in result.expected:
            expected_case, expected_traceback = expected_tuple
            self.assertIsInstance(expected_case, str)
            self.assertIsInstance(expected_traceback, str)
            self.assertEqual(case, expected_case)
            self.assertEqual(traceback, expected_traceback)
        self.assertIsInstance(result.unexpected, list)
        for unexpected_case in result.unexpected:
            self.assertIsInstance(unexpected_case, str)
            self.assertEqual(case, unexpected_case)

    def test_from_unittest_factory_method(self):
        """Test ``from_unittest`` factory method."""
        pass

    def test_qualified_name_static_method(self):
        pass

    def test_extract_tuple_static_method(self):
        pass

    def test_extract_static_method(self):
        pass


class TestTesterJSONInterface(TestCase):
    """Unit test case for ``Tester`` JSON Interface."""

    def test_from_json_factory_method(self):
        """Test ``from_json`` factory method."""
        pass

    def test_write_json_output_method(self):
        """Test ``write_json`` output method."""
        pass

    def test_write_read_cycle(self):
        """Test write - read cycle is consistent."""
        pass


class TestTesterMethods(TestCase):
    """Unit test case for ``Tester`` methods."""

    def test_successful_tests(self):
        """Test ."""
        pass

    def test_status(self):
        """Test ."""
        pass


if __name__ == "__main__":
    main()  # pragma: no cover
