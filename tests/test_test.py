#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for :py:module:`test` module."""

import unittest


class TestTester(unittest.TestCase):
    """Unit test case for ``Tester``."""

    @unittest.expectedFailure
    def test_something(self):
        """Test ..."""
        self.fail()


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
