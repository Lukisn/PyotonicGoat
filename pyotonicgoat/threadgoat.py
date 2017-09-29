#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
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


class LoopThreadBase(threading.Thread):

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.run_forever()

    def stop(self):
        self.running = False
        self.join()

    def run_forever(self):
        raise NotImplementedError


class ScannerThread(LoopThreadBase):

    def __init__(self, base, interval):
        super().__init__()
        self.interval = interval
        self.scanner = Scanner(base)  # scans initially
        self.last_change = now()

    def run_forever(self):
        if (now() - self.last_change).total_seconds() > self.interval:
            self.scan()

    def scan(self):
        if self.scanner.has_changed():
            self.last_change = self.scanner.last_time


class TesterThread(LoopThreadBase):

    def __init__(self, base):
        super().__init__()
        self.base = base
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.file = os.path.join(self.tmp_dir.name, "results.json")
        self.last_change = None
        self.last_result = None
        self.trigger_testing = False
        self.test()

    def run_forever(self):
        if self.trigger_testing:
            self.test()

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


class OutputThread(LoopThreadBase):

    def __init__(self, base=".", scan_interval=1, output_interval=0.33):
        super().__init__()
        self.output_interval = output_interval
        self.spinner = itertools.cycle("|/-\\")
        self.running = False
        self.scan_thread = ScannerThread(base=base, interval=scan_interval)
        self.test_thread = TesterThread(base=base)

    def run_forever(self):
        self.output()
        time.sleep(self.output_interval)
        if self.test_thread.last_change < self.scan_thread.last_change:
            self.test_thread.trigger_testing = True

    def run(self):
        self.scan_thread.start()
        self.test_thread.start()
        super().run()

    def stop(self):
        super().stop()
        self.scan_thread.stop()
        self.test_thread.stop()

    def output(self):
        fmt = "\r[{time}] {ind} [{status:^7s}] {green}/{run} {info}"
        if self.test_thread.last_result is None:
            status, green, run = "?", "~*~", "~*~"
        else:
            status = self.test_thread.last_result.status()
            green = self.test_thread.last_result.successful_tests()
            run = self.test_thread.last_result.testsRun

        print(fmt.format(time=now().strftime(TIME_FMT),
                         status=colored_status(status),
                         green=green, run=run, info=self.build_info(),
                         ind=next(self.spinner)),
              end="", flush=True)

    def build_info(self):
        errors = len(self.test_thread.last_result.errors)
        failures = len(self.test_thread.last_result.failures)
        skipped = len(self.test_thread.last_result.skipped)
        expected = len(self.test_thread.last_result.expected)
        unexpected = len(self.test_thread.last_result.unexpected)

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
        return "({}) ".format(", ".join(infos))


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = ArgumentParser("Run PyotonicGoat CLI")
    parser.add_argument(
        "base", type=str,
        help="Base directory to scan and run tests from")
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="scan interval in seconds")
    args = parser.parse_args(argv)
    return args


def main():
    args = parse_args()

    timestamp = now().strftime(TIME_FMT)
    print(f"[{timestamp}] starting up ... (exit with CTRL-C)")

    output = OutputThread(base=args.base, scan_interval=args.interval)
    output.start()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            timestamp = now().strftime(TIME_FMT)
            print(f"\n[{timestamp}] shutting down ...")
            output.stop()
            break


if __name__ == "__main__":
    main()

