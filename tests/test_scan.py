#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`scan` module."""

from os.path import abspath, dirname, basename, exists
import unittest
import fs.tempfs as tempfs
from scan import Scanner

LOCATION = dirname(abspath(__file__))


class TestScannerInstantiation(unittest.TestCase):
    """Unit test case for ``Scanner`` initialization."""

    def test_init_raises_on_nonexisting_dir(self):
        """Test ``Scanner`` init raises on non existing dir."""
        non_existing_dir = "./this/does/not/exist/"
        assert not exists(non_existing_dir)
        with self.assertRaises(IOError):
            _ = Scanner(base=non_existing_dir)

    def test_init_succeeds_on_existing_dir(self):
        """Test ``Scanner`` init succeeds on existing dir."""
        scanner = Scanner(base=LOCATION)
        self.assertIn(__file__, scanner.last_result)


class TestScannerBehavior(unittest.TestCase):
    """Test case for ``Scanner`` beahavior."""

    def setUp(self):
        """Set up test fixture.

        Create a temporary directory tree to scan and manipulate.
        """
        # create temporary directory tree
        print("creating temp dir tree in '{}'".format(LOCATION))
        self.tfs = tempfs.TempFS(temp_dir=LOCATION)
        self.base = self.tfs.desc("/")
        print("temp dir '{}' created".format(self.base))
        # create scanner
        self.scanner = Scanner(base=self.base)

    def tearDown(self):
        """Tear down test fixture.

        Close and thereby remove the temporary directory tree.
        """
        print("closing temp dir tree in '{}'".format(self.tfs.desc("/")))
        self.tfs.close()

    def test_something(self):
        """Test..."""
        print("current dir tree:")
        print(self.tfs.tree())


if __name__ == "__main__":
    unittest.main()
