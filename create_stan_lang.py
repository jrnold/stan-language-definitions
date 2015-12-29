""" Extract function sign

- If new manual, may need to adjust any code that has hardcoded sections.

"""
import csv
import json
import re
import sys
import glob

import yaml

arg_types = (
    "reals?",
    "ints?",
    "(?:(?:row|col)_)?vector",
    "matrix",
    "T"
)

##########

def parse_args(argtext):
    if argtext != "()":
        arg_type = r"(?:" + r"|".join(arg_types) + ")"
        arg_name = "[A-Za-z][A-Za-z0-9_]*(?:\[.*\])?"
        arg_regex = re.compile(r"(?P<type>%s(?:\[(?:\.{3}|,)?\])?)\s+(?P<name>%s)" % (arg_type, arg_name))
        matches = arg_regex.findall(argtext)
        if not len(matches):
            print("Could not find any matches: %s" % argtext)
        ret = [{'type': x[0], 'name': x[1]} for x in matches]
    else:
        ret = []
    return ret

def parse_functions(src, special_functions):

    with open(src, "r") as f:
        reader = csv.reader(f, delimiter = ';')
        data = [row for row in reader][2:]

    distributions = set()
    functions = {}
    constants = set()

    for row in data:
        funname, funargs, funret = row[:3]
        if funargs == "~":
            distributions.add(funname)
        else:
            if funname in special_functions:
                continue
            else:
                args = parse_args(funargs)
            f = {
                'name': funname,
                'return': funret,
                'args': args,
            }
            if len(f['args']) == 0:
                constants.add(funname)
            signature = ','.join(x['type'] for x in f['args'])
            if funname not in functions:
                functions[funname] = {}
            functions[funname][signature] = f
    return (functions,
            sorted(list(distributions)),
            sorted(list(constants)))

def build(file_functions, file_keywords, dst):
    print("functions file: %s" % file_functions)
    with open(file_keywords, 'r') as f:
        data = yaml.load(f)
    functions, distributions, constants = parse_functions(file_functions, data['keywords']['functions'])
    version = re.search(r"-([0-9]+\.[0.9]+\.[0-9]+)\.txt$", file_functions).group(1)
    print("Stan version: %s" % version)
    data['version'] = version
    data['functions'] = functions
    data['distributions'] = distributions
    data['constants'] = constants
    with open(dst, 'w') as f:
        json.dump(data, f, sort_keys = True, indent = 2, separators = (',', ': '))

def main():
    dst = sys.argv[1]
    file_functions = glob.glob("stan/doc/stan-functions-*.txt")[0]
    file_keywords = 'stan-lang-keywords.yaml'
    build(file_functions, file_keywords, dst)

if __name__ == '__main__':
    main()
