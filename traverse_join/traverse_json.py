#!/usr/bin/env python3

# Python 2 & 3 compatible
from __future__ import print_function
from six import iteritems
from builtins import range

import json
import requests
import collections
import traverse_json.utils as utils


class JsonTraverse(object):
    """
    JSON traverse

    Parameters
    ----------
    @filepath: str
        Path to the JSON file
    @url: str
        URL to the JSON. Either `filepath` or `url` needs to be specified
    @ignore_case: bool
        Whether to ignore cases. Default ignores case
    @separator: str
        Separator used in the path to traverse the JSON. Default is '/'
    @kwargs:
        Additional keyword arguments for `open()` (when `filepath` is given)
        or `requests.get()` (when `url` is given)
    """
    def __init__(self, filepath=None,
                 url=None,
                 json_data=None,
                 ignore_case=True,
                 separator='/',
                 **kwargs):
        super(JsonTraverse, self).__init__()
        error_message = 'Provide one of filepath, url or json_data!'
        assert filepath or url or json_data, error_message
        self.ignore_case = ignore_case
        self.separator = separator
        if filepath:
            self.read_json_from_file(filepath, **kwargs)
        elif url:
            self.read_json_from_url(url, **kwargs)
        else:
            self.json = json_data

    def read_json_from_file(self, filepath, **kwargs):
        valid_json_file = (utils.is_valid_file(filepath) and
                           utils.file_ext(filepath) == '.json')
        assert valid_json_file, 'Invalid JSON file path provided!'
        with open(filepath, 'r', **kwargs) as file:
            try:
                data = json.load(file)
            except Exception:
                print('Invalid JSON file')
        self.json = data

    def read_json_from_url(self, url, **kwargs):
        response = requests.get(url, **kwargs)
        try:
            data = json.loads(response.text)
        except Exception:
            print('URL to invalid JSON!')
        self.json = data

    @staticmethod
    def get_value_from_dict(adict, string_key, ignore_case=False, named=True):
        """
        Gets value from {key: value} pair in a dictionary by key

        Parameters
        ----------
        @adict: dict
            A dictionary whose keys are of string type
        @string_key: str
            A key of the dictionary or a regular expression pattern that can
            match one or more keys
        @ignore_case: bool
            Whether to ignore cases. Default ignores case
        @named: bool
            If `True` (default), returns a dictionary; otherwise returns a list
        """
        assert isinstance(adict, dict), "Getting value from a nondict"
        matched_keys = utils.re_match(string_key, adict.keys(), ignore_case)
        if named:
            result = {
                matched_key: adict[matched_key]
                for matched_key in matched_keys
            }
        else:
            result = [adict[matched_key] for matched_key in matched_keys]
        return result

    @staticmethod
    def get_element_from_list(alist, string_index, named=True):
        """
        Gets element(s) from a list

        Parameters
        ----------
        @alist: list / collections.Iterable
            A list or an iterable
        @string_index: str
            String representation of index to slice the list. See examples
            below
        @named: bool
            If `True` (default), returns a `collections.OrderedDict`;
            otherwise returns a list

        Examples
        --------
        > from traverse_json import JsonTraverse
        > JsonTraverse.get_element_from_list(range(10), ':5')
        > OrderedDict([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
        >
        > JsonTraverse.get_element_from_list(range(10), ':5', named=False)
        > range(0, 5)
        """
        error_message = 'Getting element from a non-list/iterable'
        assert isinstance(alist, (list, collections.Iterable)), error_message
        slice_index = utils.slice_from_string(string_index)
        if named:
            result = collections.OrderedDict(zip(
                list(range(len(alist)))[slice_index],
                alist[slice_index]
            ))
        else:
            result = alist[slice_index]
        return result

    def _traverse_next(self, json_data, string, named=True):
        can_go_down = isinstance(json_data, (dict, list))
        assert can_go_down, 'Can not traverse down the json data'
        if isinstance(json_data, dict):
            return self.get_value_from_dict(json_data,
                                            string,
                                            self.ignore_case,
                                            named)
        else:
            return self.get_element_from_list(json_data, string, named)

    def traverse(self, path, named=True):
        """
        Traverses a json if it were a filesystem

        Parameters
        ----------
        @path: str
            A search path. Examples are (when `self.separator` == '/')
            - 'an/path/example' ('an' -> 'path' -> 'example')
            - 'path/with/1/element' ('path' -> 'with' -> '[1]' -> 'element')
        @named: bool
            If `True` (default), returns a `collections.OrderedDict`;
            otherwise returns a list

        Notes
        -----
        When proceeding with a dictionary, provide a string key or a regular
        expression pattern
        When proceeding with a list, provide a string index. Examples are found
        in utils.slice_from_string()
        """
        separator = self.separator
        result = {'': self.json} if named else [self.json]
        steps = path.split(separator)
        for step in steps:
            if named:
                result = collections.OrderedDict(
                    ((ppath + separator + str(cpath)).strip(separator), value)
                    for ppath, pjson in iteritems(result)
                    for cpath, value in iteritems(self._traverse_next(pjson,
                                                                      step,
                                                                      True))
                )
            else:
                result = [
                    value for pjson in result
                    for value in self._traverse_next(pjson, step, False)
                ]
        return result
