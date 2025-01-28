#!/usr/bin/env python3

import inspect


def create_file(file):
    '''A function that creates a new report file each time the
    script is run'''
    with open(file, 'w') as f:
        return


def generate_report(results, file='report.txt'):
    '''A function that appends results to file
    '''
    with open(file, 'w') as f:
        json.dump(results, f, indent=4)
        f.write('\n')
    print(f'Data has been written to {file}')

    return 0

def get_args(func):
    '''get auguments from each model function'''
    args = inspect.getfullargspec(func).args[1:]
    return args