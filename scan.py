#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scanner."""

import datetime
from os import walk, stat
from os.path import abspath, join, isdir


class Scanner:
    """Simple Directory scanner."""

    def __init__(self, base):
        """Initializer."""
        if not isdir(base):
            raise IOError("Base dir '{}' does not exist!".format(base))
        self.base = base
        self.last_time = None
        self.last_result = None
        self.scan()  # initialize scanner with first scan data

    def scan(self):
        """Scan the directory tree.

        returns the scan data in a flat dictionary where the keys are the file
        names with full absolute paths and the values are ``stat_info`` objects
        containing the relevant information. Also save the scan in the
        ``last_scan`` property of the object and the scan time in the
        ``last_time`` property.
        """
        scan = {}  # {"full/path/file.name": <stat_info object>}
        for path, _, files in walk(self.base):  # directories not needed
            path = abspath(path)
            for fname in files:
                full_path = join(path, fname)
                stat_info = stat(full_path)
                scan[full_path] = stat_info
        self.last_time = datetime.datetime.now()
        self.last_result = scan
        return scan

    def has_changed(self):
        """Check if the directory tree has changed since the last scan."""
        last_result = self.last_result
        current_result = self.scan()
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
