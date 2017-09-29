#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest


@unittest.skip("remove all example tests")
class ExampleTestCase(unittest.TestCase):

    def test_success(self):
        time.sleep(1)
        pass

    @unittest.skip("remove failure")
    def test_failure(self):
        self.fail()

    @unittest.skip("remove error")
    def test_error(self):
        raise RuntimeError("Unexpected Error")

    @unittest.skip("test skipping")
    def test_skipped(self):
        pass

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.fail()

    @unittest.skip("remove unexpected success")
    @unittest.expectedFailure
    def test_unexpected_success(self):
        pass
