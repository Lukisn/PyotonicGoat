#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scanner."""

import datetime
from os import walk, stat
from os.path import abspath, join, isdir


class Scanner():
    """Simple Ddirectory scanner."""

    def __init__(self, base):
        """Initializer."""
        if not isdir(base):
            raise IOError("Base dir '{}' does not exist!".format(base))
        self.base = base
        self.last_time = datetime.datetime.now()
        self.last_result = self.scan()

    def has_changed(self):
        """Check if the directory tree has changed since the last scan."""
        current_result = self.scan()
        last_result = self.last_result
        self.last_result = current_result
        # STEP 1: check number of files:
        if len(current_result) > len(last_result):
            return True  # new files added
        elif len(current_result) < len(last_result):
            return True  # files removed
        else:  # lengths are equal
            # STEP 2: check file names:
            if sorted(current_result.keys()) != sorted(last_result.keys()):
                return True  # file name changed or file moved
            else:  # file names are not changed -> check contents
                for fname, stat_info in current_result.items():
                    if stat_info != last_result[fname]:
                        return True  # file contents have changed
        return False  # nothing has changed

    def scan(self):
        """Scan the directory tree.

        returns the scan data in a flat dictionary where the keys are the file
        names with fullabsolute paths and the keys are ``stat_info`` objects
        containing the relevant information.
        """
        scan = {}  # {"full/path/file.name": <stat_info object>}
        for path, _, files in walk(self.base):  # directories not needed
            path = abspath(path)
            for fname in files:
                full_path = join(path, fname)
                stat_info = stat(full_path)
                scan[full_path] = stat_info
        return scan


if __name__ == "__main__":
    import tempfile
    scanner = Scanner(base="./test_dir/")
    print(scanner.has_changed(), "False?")
    tfile = tempfile.NamedTemporaryFile(dir="./test_dir/", mode="w+t")
    print(scanner.has_changed(), "True?")
    tfile.write("askdkalsdkkald")
    tfile.flush()
    print(scanner.has_changed(), "True?")
    tfile.close()
    print(scanner.has_changed(), "True?")
    print(scanner.has_changed(), "False?")
