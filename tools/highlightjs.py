#!/usr/bin/env python
"""
Create the file _stan_builtins.py used in the `pygments` package from `stan_lang.json`.
"""
import json
import sys
import textwrap

def tostr(x):
    out = '[' + ', '.join(f"'{i}'" for i in x) + ']'
    return '\n'.join(textwrap.wrap(out, 80))

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    functions = sorted([k for k, v in data['functions'].items()
                        if not v['operator']])
    distributions = sorted([v['sampling']
                            for k, v in data['functions'].items()
                            if v['sampling']])
    return {
        'distributions': distributions,
        'functions': functions,
    }

def create_code(data):
    print("const FUNCTIONS = {};".format(tostr(data['functions'])))
    print("const DISRIBUTIONS = {};".format(tostr(data['distributions'])))

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    create_code(data)
