#!/usr/bin/env python3

# mausy5043-common
# Copyright (C) 2025  Maurice (mausy5043) Hendrix
# AGPL-3.0-or-later  - see LICENSE

"""Provide file operation functions."""

import os
import syslog
import warnings


def cat(file_name: str) -> str:
    """Read a file (line-by-line) into a variable.

    Args:
        file_name (str) : file to read from

    Returns:
          (str) : file contents
    """
    contents: str = ""
    if os.path.isfile(file_name):
        with open(file_name, encoding="utf-8") as file_stream:
            contents = file_stream.read().strip("\n")
    return contents


def syslog_trace(trace: str, logerr: int, out2console: bool = False) -> None:
    """Log a (multi-line) message to syslog.

    Initialise with a call to
    syslog.openlog(ident=<string>, facility=<syslog.facility>)

    Args:
        trace (str): Text to send to log
        logerr (int): syslog errornumber
        out2console (bool): If True, will also print the 'trace' to the screen

    Returns:
        None
    """
    warnings.warn(
        "This function is deprecated. Use logging instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    log_lines: list[str] = trace.split("\n")
    for line in log_lines:
        if line and logerr:
            syslog.syslog(logerr, line)
        if line and out2console:
            print(line)
