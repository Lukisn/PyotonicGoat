#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`scan` module."""

from unittest import TestCase, main, skip
from datetime import datetime
from os.path import abspath, dirname, exists, join
from shutil import move
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pyotonicgoat.scanning import Scanner

HERE = dirname(abspath(__file__))


class TestScannerInstantiation(TestCase):
    """Unit test case for ``Scanner`` initialization."""

    def test_init_raises_on_non_existing_dir(self):
        """Test ``Scanner`` init raises on non existing dir."""
        non_existing_dir = "./this/does/not/exist/"
        assert not exists(non_existing_dir)
        with self.assertRaises(IOError):
            _ = Scanner(base=non_existing_dir)

    def test_init_succeeds_on_existing_dir(self):
        """Test ``Scanner`` init succeeds on existing dir."""
        scanner = Scanner(base=HERE)
        self.assertIsInstance(scanner.last_time, datetime)
        self.assertIsInstance(scanner.last_result, dict)
        self.assertIn(__file__, scanner.last_result)


@skip("causes FileNotFoundErrors")
class TestScannerBehavior(TestCase):
    """Test case for ``Scanner`` behavior."""

    def setUp(self):
        """Set up test fixture.

        Create a temporary directory tree to scan and manipulate.
        """
        self.temp_dir = TemporaryDirectory()
        assert exists(self.temp_dir.name)
        self.scanner = Scanner(base=self.temp_dir.name)

    def tearDown(self):
        """Tear down test fixture.

        Close and thereby remove the temporary directory tree.
        """
        self.temp_dir.cleanup()
        assert not exists(self.temp_dir.name)

    def setup_directory_tree(self):
        """Set up content for the temporary directory tree.

            temp_dir_root/
                file
                subdir/
                    file
                    subsubdir/
                    file
                emptysubdir/
        """
        self.subdir = TemporaryDirectory(dir=self.temp_dir.name)
        self.subsubdir = TemporaryDirectory(dir=self.subdir.name)
        self.empty_subdir = TemporaryDirectory(dir=self.temp_dir.name)
        self.temp_file = NamedTemporaryFile(
            dir=self.temp_dir.name, mode="w+t")
        self.temp_file.write("This is original content\n")
        self.temp_file.flush()
        self.subdir_temp_file = NamedTemporaryFile(
            dir=self.subdir.name, mode="w+t")
        self.subdir_temp_file.write("This is original content\n")
        self.subdir_temp_file.flush()
        self.subsubdir_temp_file = NamedTemporaryFile(
            dir=self.subsubdir.name, mode="w+t")
        self.subsubdir_temp_file.write("This is original content\n")
        self.subsubdir_temp_file.flush()
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
        _ = NamedTemporaryFile(dir=self.temp_dir.name)
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_added_file_in_subdir_succeeds(self):
        """Test if an added file in a subdir is detected by the scanner."""
        subdir = TemporaryDirectory(dir=self.temp_dir.name)
        _ = NamedTemporaryFile(dir=subdir.name)
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_removed_file_succeeds(self):
        """Test if a removed file is detected by the scanner."""
        self.setup_directory_tree()
        self.temp_file.close()
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_removed_file_in_subdir_succeeds(self):
        """Test if a removed file in a subdir  is detected by the scanner."""
        self.setup_directory_tree()
        self.subdir_temp_file.close()
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_renamed_file_succeeds(self):
        """Test if renaming a file is detected by the scanner."""
        self.setup_directory_tree()
        target = join(dirname(self.temp_file.name), "renamed_file")
        move(self.temp_file.name, target)
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_renamed_dir_succeeds(self):
        """Test if renaming a directory is detected by the scanner."""
        self.setup_directory_tree()
        target = join(self.temp_dir.name, "renamed_subdir/")
        move(self.subdir.name, target)
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_changed_file_succeeds(self):
        """Test if changing a file's content is detected by the scanner."""
        self.setup_directory_tree()
        self.temp_file.write("This is new content\n")
        self.temp_file.flush()
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())

    def test_scanning_changed_file_in_subdir_succeeds(self):
        """Test if changing a file's content in a subdir is detected."""
        self.setup_directory_tree()
        self.subdir_temp_file.write("This is new content\n")
        self.subdir_temp_file.flush()
        self.assertTrue(self.scanner.has_changed())
        self.assertFalse(self.scanner.has_changed())


if __name__ == "__main__":
    main()  # pragma: no cover
