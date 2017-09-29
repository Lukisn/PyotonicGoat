#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from time import sleep
from threading import Thread
from pyotonicgoat.util import now, colored, colored_status
from pyotonicgoat.scanning import Scanner
from pyotonicgoat.testing import Tester


TIME_FMT = "%H:%M:%S"


class LoopThreadBase(Thread):

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
        self.tester = Tester(base)
        self.last_change = now()
        self.trigger_testing = False

    def run_forever(self):
        if self.trigger_testing:
            self.test()

    def test(self):
        self.tester.test()
        self.trigger_testing = False

    def status(self):
        return (self.tester.last_result.status(),
                self.tester.last_result.green(),
                self.tester.last_result.testsRun)

    def info(self):
        infos = []

        # errors preventing testing in the first place:
        errors = len(self.tester.last_result.errors)
        if errors:
            infos.append(colored(f"{errors} errors", "yellow"))

        # failures and unexpected succcesses are considered failures:
        failures = len(self.tester.last_result.failures)
        if failures:
            infos.append(colored(f"{failures} errors", "red"))
        unexpected = len(self.tester.last_result.unexpected)
        if unexpected:
            infos.append(colored(f"{unexpected} unexpected success", "red"))

        # skipped and expected failures are only for information:
        skipped = len(self.tester.last_result.skipped)
        if skipped:
            infos.append(f"{skipped} skipped")
        expected = len(self.tester.last_result.expected)
        if expected:
            infos.append(f"{expected} xfails")

        # build comma separated list string from given information list:
        return "({}) ".format(", ".join(infos))


class OutputThread(LoopThreadBase):

    def __init__(self, base=".", scan_interval=1, output_interval=0.33):
        super().__init__()
        self.output_interval = output_interval
        self.running = False
        self.scan_thread = ScannerThread(base=base, interval=scan_interval)
        self.test_thread = TesterThread(base=base)

    def run_forever(self):
        self.output()
        sleep(self.output_interval)
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
        fmt = "\r[{time}] [{status:}] {green}/{run} {info}"
        status, green, run = self.test_thread.status()
        print(fmt.format(
            time=now().strftime(TIME_FMT),
            status=colored_status(status), green=green, run=run,
            info=self.test_thread.info()), end="", flush=True)


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
            sleep(10)
        except KeyboardInterrupt:
            timestamp = now().strftime(TIME_FMT)
            print(f"\n[{timestamp}] shutting down ...")
            output.stop()
            break


if __name__ == "__main__":
    main()
