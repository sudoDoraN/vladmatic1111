#!/bin/env python
"""
generic helper methods
"""

import string
import logging

log_format = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level = logging.INFO, format = log_format)
log = logging.getLogger("sd")


def set_logfile(logfile):
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(log_format)
    fh.setLevel(log.getEffectiveLevel())
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.info({ 'log file': logfile })


def safestring(text: str):
    lines = []
    for line in text.splitlines():
        lines.append(line.translate(str.maketrans('', '', string.punctuation)).strip())
    res = ', '.join(lines)
    return res[:1000]


class Map(dict):
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        v = Map(v)
                    if isinstance(v, list):
                        self.__convert(v)
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    v = Map(v)
                elif isinstance(v, list):
                    self.__convert(v)
                self[k] = v
    def __convert(self, v):
        for elem in range(0, len(v)): # pylint: disable=consider-using-enumerate
            if isinstance(v[elem], dict):
                v[elem] = Map(v[elem])
            elif isinstance(v[elem], list):
                self.__convert(v[elem])
    def __getattr__(self, attr):
        return self.get(attr)
    def __setattr__(self, key, value):
        self.__setitem__(key, value)
    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})
    def __delattr__(self, item):
        self.__delitem__(item)
    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


if __name__ == "__main__":
    pass
