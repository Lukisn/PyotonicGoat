#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`test` module."""

import datetime
from fs import tempfs
from os.path import abspath, dirname, exists, join
import unittest
from test import Tester

LOCATION = join(dirname(abspath(__file__)))


class TestTesterInitialization(unittest.TestCase):
    """Unit test case for ``Tester`` initialization."""

    def setUp(self):
        """Set up test fixture."""
        self.tfs = tempfs.TempFS(temp_dir=LOCATION)
        self.base = self.tfs.desc("/")
        assert exists(self.base)

    def tearDown(self):
        """Tear down test fixture."""
        self.tfs.close()
        assert not exists(self.base)

    def test_init_raises_on_nonexisting_dir(self):
        """Test ``Tester`` init raises on non existing dir."""
        non_existing_dir = "./this/does/not/exist/"
        assert not exists(non_existing_dir)
        with self.assertRaises(IOError):
            _ = Tester(base=non_existing_dir)

    def test_init_succeeds_on_existing_dir(self):
        """Test ``Tester`` init succeeds on existing dir."""
        tester = Tester(base=self.base)
        self.assertIsInstance(tester.last_time, datetime.datetime)
        self.assertIsInstance(tester.last_result, unittest.TextTestResult)


class TestTesterBehavior(unittest.TestCase):
    """Unit test case for ``Tester`` behavior."""

    EXAMPLES = """
class ExampleTestCases(unittest.TestCase):

    def test_success(self):
        pass

    def test_error(self):
        raise RuntimeError("testing error")

    def test_failure(self):
        self.fail()

    @unittest.skip("skip for testing")
    def test_skipped(self):
        pass

    @unittest.expectedFailure
    def test_expectedFailure(self):
        self.fail()

    @unittest.expectedFailure
    def test_unexpectedSuccess(self):
        pass
"""
    # test case class containing 6 tests: 1x successful
    #                                     1x error
    #                                     1x failure
    #                                     1x skipped
    #                                     1x expected failure
    #                                     1x unexpected success

    def setUp(self):
        """Set up test fixture."""
        self.tfs = tempfs.TempFS(temp_dir=LOCATION)
        self.base = self.tfs.desc("/")
        assert exists(self.base)
        self.tfs.create("test_something.py")
        with self.tfs.open("test_something.py", mode="wt") as fh:
            fh.write(self.EXAMPLES)
        assert exists(join(self.base, "test_something.py"))
        # create tester
        self.tester = Tester(base=self.base)

    def tearDown(self):
        """Tear down test fixture."""
        self.tfs.close()
        assert not exists(self.base)

    # TODO: write unit tests for Tester behavior
    def test_(self):
        """Test ."""
        pass


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
