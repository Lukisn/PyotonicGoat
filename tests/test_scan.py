#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`scan` module."""

from datetime import datetime
from os.path import abspath, dirname, exists
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
        self.assertIsInstance(scanner.last_time, datetime)
        self.assertIsInstance(scanner.last_result, dict)
        self.assertIn(__file__, scanner.last_result)


class TestScannerBehavior(unittest.TestCase):
    """Test case for ``Scanner`` beahavior."""

    def setUp(self):
        """Set up test fixture.

        Create a temporary directory tree to scan and manipulate.
        """
        # create temporary directory tree
        # print("creating temp dir tree in '{}'".format(LOCATION))
        self.tfs = tempfs.TempFS(temp_dir=LOCATION)
        self.base = self.tfs.desc("/")
        # print("temp dir '{}' created".format(self.base))
        assert exists(self.base)
        # create scanner
        self.scanner = Scanner(base=self.base)

    def tearDown(self):
        """Tear down test fixture.

        Close and thereby remove the temporary directory tree.
        """
        # print("closing temp dir tree in '{}'".format(self.tfs.desc("/")))
        self.tfs.close()
        assert not exists(self.base)

    def setup_directory_tree(self):
        """Set up content for the temporary directory tree.

            tmp_dir_root/
                file
                subdir/
                    file
                    subsubdir/
                    file
                emptysubdir/
        """
        self.tfs.makedirs("subdir/subsubdir/")
        self.tfs.makedir("emptysubdir/")
        self.tfs.create("file")
        with self.tfs.open("file", mode="wt") as fh:
            fh.write("This is original content\n")
        self.tfs.create("subdir/file")
        with self.tfs.open("subdir/file", mode="wt") as fh:
            fh.write("This is original content\n")
        self.tfs.create("subdir/subsubdir/file")
        with self.tfs.open("subdir/subsubdir/file", mode="wt") as fh:
            fh.write("This is original content\n")
        self.scanner.scan()  # capture current state

    def test_scanning_unchanged_empty_dir_succeeds(self):
        """Test if scanning an unchanged empty dir succeeds."""
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_unchanged_dir_succeeds(self):
        """Test if scanning an unchanged empty dir succeeds."""
        self.setup_directory_tree()
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_added_file_succeeds(self):
        """Test if an added file is detected by the scanner."""
        self.tfs.create("file")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_added_file_in_subdir_succeeds(self):
        """Test if an added file in a subdir is detected by the scanner."""
        self.tfs.makedir("subdir/")
        self.tfs.create("subdir/file")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_removed_file_succeeds(self):
        """Test if a removed file is detected by the scanner."""
        self.setup_directory_tree()
        self.tfs.remove("file")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_removed_file_in_subdir_succeeds(self):
        """Test if a removed file in a subdir  is detected by the scanner."""
        self.setup_directory_tree()
        self.tfs.remove("subdir/file")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_renamed_file_succeeds(self):
        """Test if renaming a file is detected by the scanner."""
        self.setup_directory_tree()
        self.tfs.move("file", "renamed_file")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_renamed_dir_succeeds(self):
        """Test if renaming a directory is detected by the scanner."""
        self.setup_directory_tree()
        self.tfs.makedir("renamed_subdir/")
        self.tfs.movedir("subdir/", "renamed_subdir/")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_changed_file_succeeds(self):
        """Test if changing a file's content is detected by the scanner."""
        self.setup_directory_tree()
        with self.tfs.open("file", mode="at") as fh:
            fh.write("This is new content\n")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_changed_file_in_subdir_succeeds(self):
        """Test if changing a file's content in a subdir is detected."""
        self.setup_directory_tree()
        with self.tfs.open("subdir/file", mode="at") as fh:
            fh.write("This is new content\n")
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
