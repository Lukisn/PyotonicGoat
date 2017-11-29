#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from unittest import TestCase, skip, expectedFailure


@skip("remove all example tests")
class ExampleTestCase(TestCase):

    def test_success(self):
        sleep(1)
        pass

    # @skip("remove failure")
    def test_failure(self):
        self.fail()

    # @skip("remove error")
    def test_error(self):
        raise RuntimeError("Error during test method")

    # @skip("test skipping")
    def test_skipped(self):
        pass

    @expectedFailure
    def test_expected_failure(self):
        self.fail()

    # @skip("remove unexpected success")
    @expectedFailure
    def test_unexpected_success(self):
        pass
