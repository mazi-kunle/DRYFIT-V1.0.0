#!/usr/bin/env python3

import inspect


def get_args(func):
    '''get auguments from each model function'''
    args = inspect.getfullargspec(func).args[1:]
    return args