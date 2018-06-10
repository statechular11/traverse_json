#!/usr/bin/env python3

import os
import re


def parse_path(path):
    """
    Note
    ----
    `os.path.expanduser`: On Unix and Windows, return the argument with an
        initial component of ~ or ~user replaced by that user’s home directory.
    `os.path.realpath`: Return the canonical path of the specified filename,
        eliminating any symbolic links encountered in the path.

    The function will take care of '~', '.', '..' and symbolic links in the
    path
    """
    return os.path.realpath(os.path.expanduser(path))


def is_valid_file(file_path):
    """
    Checks if the file path is a path to a valid file
    """
    file_path = parse_path(file_path)
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def is_string_int(string):
    """
    Checks if the string is a valid representation of an integer

    Examples
    --------
    > is_string_int('12')
    > True
    >
    > is_string_int('a')
    > False
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def re_match(pattern, alist, ignore_case=False):
    """
    Filters a list with a regexpr pattern and returns an iterator

    Paramters
    ---------
    @pattern: str
        Regular expression pattern
    @alist: list
        A list to filter
    @ignore_case: bool
        Whether to ignore cases. Default ignores case

    Examples
    --------
    > list(re_match('ab\.*', ['abc', 'about', 'adobe']))
    > ['abc', 'about']
    """
    flags = re.IGNORECASE if ignore_case else 0
    return filter(re.compile(pattern, flags=flags).match, alist)


def file_ext(file_path):
    """
    Returns file extension

    Examples
    --------
    > file_ext('test.json')
    > '.json'
    """
    file_path = parse_path(file_path)
    return os.path.splitext(file_path)[1]


def slice_from_string(string):
    """
    Returns slice object from string representation.

    Examples
    --------
    > slice_from_string('0')
    > slice(0, 1, None)
    >
    > slice_from_string(':')
    > slice(None, None, None)
    >
    > slice_from_string(':5')
    > slice(None, 5, None)
    >
    > slice_from_string('5:')
    > slice(5, None, None)
    >
    > slice_from_string('3:9')
    > slice(3, 9, None)
    >
    > slice_from_string('3:9:2')
    > slice(3, 9, 2)
    >
    > slice_from_string('3:a')
    > AssertionError: Only digits and colon are allowed in the input string
    """
    splits = [char.strip() for char in string.split(':')]
    input_cond = all(is_string_int(char) or char == '' for char in splits)
    assert input_cond, 'Only digits and colon are allowed in the input string'
    assert len(splits) <= 3, 'Invalid parameters for slice()'
    params_for_slice = [int(char) if char else None for char in splits]
    if len(params_for_slice) == 1:
        if params_for_slice[0] is not None:
            return slice(params_for_slice[0], params_for_slice[0] + 1)
    return slice(*params_for_slice)
