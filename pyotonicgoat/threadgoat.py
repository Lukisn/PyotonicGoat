#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import os
import subprocess
import tempfile
import time
import threading
from pyotonicgoat.util import now, colored, colored_status
from pyotonicgoat.scanning import Scanner
from pyotonicgoat.testing import ResultAdapter

TIME_FMT = "%H:%M:%S"


class ScannerThread(threading.Thread):

    def __init__(self, base, interval):
        super().__init__()
        self.interval = interval
        self.last_change = now()
        self.scanner = Scanner(base)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.scan()
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.join()

    def scan(self):
        if self.scanner.has_changed():
            self.last_change = self.scanner.last_time


class TesterThread(threading.Thread):

    def __init__(self, base):
        super().__init__()
        self.base = base
        self.tmp = tempfile.TemporaryDirectory()
        self.file = os.path.join(self.tmp.name, "results.json")
        self.last_change = None
        self.last_result = None
        self.trigger_testing = False
        self.test()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if self.trigger_testing:
                self.test()

    def stop(self):
        self.running = False
        self.join()

    def test(self):
        subprocess.run(
            ["python3", "testing.py", self.base, "-o", self.file])
        result = ResultAdapter.from_json(self.file)
        self.last_change = now()
        self.last_result = result
        self.trigger_testing = False

    def status(self):
        if self.last_result is None:
            return "initial"
        else:
            return self.last_result.status()


class OutputThread(threading.Thread):

    def __init__(self, base=".", scan_interval=1, output_interval=0.33):
        super().__init__()
        self.output_interval = output_interval
        self.spinner = itertools.cycle("|/-\\")
        self.running = False
        self.scan_thread = ScannerThread(base=base, interval=scan_interval)
        self.test_thread = TesterThread(base=base)

    def run(self):
        self.scan_thread.start()
        self.test_thread.start()
        self.running = True
        while self.running:
            self.output()
            time.sleep(self.output_interval)
            if self.test_thread.last_change < self.scan_thread.last_change:
                self.test_thread.trigger_testing = True

    def stop(self):
        self.running = False
        self.scan_thread.stop()
        self.test_thread.stop()
        self.join()

    def output(self):
        fmt = "\r[{time}] {ind} [{status:^7s}] {green}/{run} {info}"
        if self.test_thread.last_result is None:
            status, green, run = "?", "~*~", "~*~"
        else:
            status = self.test_thread.last_result.status()
            green = self.test_thread.last_result.successful_tests()
            run = self.test_thread.last_result.testsRun

        # construct additional info string:
        info = ""
        errors = len(self.test_thread.last_result.errors)
        failures = len(self.test_thread.last_result.failures)
        skipped = len(self.test_thread.last_result.skipped)
        expected = len(self.test_thread.last_result.expectedFailures)
        unexpected = len(self.test_thread.last_result.unexpectedSuccesses)

        infos = []
        if errors > 0:
            error_info = colored("{} errors".format(errors), "yellow")
            infos.append(error_info)
        if failures > 0:
            failure_info = colored("{} failures".format(failures), "red")
            infos.append(failure_info)
        if unexpected > 0:  # unexpected Successes are failures too!
            unexpected_info = colored(
                "{} unexpected success".format(unexpected),
                "red")
            infos.append(unexpected_info)
        if skipped > 0:
            skipped_info = "{} skipped".format(skipped)
            infos.append(skipped_info)
        if expected > 0:
            expected_info = "{} xfails".format(expected)
            infos.append(expected_info)
        info = "({}) ".format(", ".join(infos))

        print(fmt.format(time=now().strftime(TIME_FMT),
                         status=colored_status(status),
                         green=green, run=run, info=info,
                         ind=next(self.spinner)),
              end="", flush=True)


def main():
    timestamp = now().strftime(TIME_FMT)
    print(f"[{timestamp}] starting up... (exit with CTRL-C)")

    output = OutputThread("..")
    output.start()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print()
            timestamp = now().strftime(TIME_FMT)
            print(f"[{timestamp}] shutting down ...")
            output.stop()
            break


if __name__ == "__main__":
    main()
