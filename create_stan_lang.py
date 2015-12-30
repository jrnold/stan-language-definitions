""" Extract function sign

- If new manual, may need to adjust any code that has hardcoded sections.

"""
import csv
import json
import re
import sys
import glob

import yaml


def parse_args(argtext):
    if argtext == "()":
        ret = []
    elif argtext == "~":
        ret = None
    else:
        # It needs to be this complicated because of the bracketsnn
        arg_type = r"(?P<type>[A-Za-z_]+(?:\[.*?\])?)"
        arg_name = r"(?P<name>[A-Za-z][A-Za-z0-9_]*(?:\[.*?\])?)"
        arg_regex = re.compile(r"%s\s+%s" % (arg_type, arg_name))
        matches = arg_regex.findall(argtext)
        if not len(matches):
            print("Could not find any matches: %s" % argtext)
        ret = [{'type': x[0], 'name': x[1]} for x in matches]
    return ret

def parse_functions(src, data):

    with open(src, "r") as f:
        reader = csv.reader(f, delimiter = ';')
        fundata = [row for row in reader][2:]

    functions = {}
    distributions = set()

    for row in fundata:
        funname, funargs, funret = row[:3]
        if funname == "multi_normal":
            print(row)
        if funargs == "~":
            distributions.add(funname)
        else:
            if funname in data['keywords']['functions']:
                continue
            else:
                args = parse_args(funargs)
                f = {
                    'name': funname,
                    'return': funret,
                    'args': args,
                }
                signature = ','.join(x['type'] for x in f['args'])
                if funname not in functions:
                    functions[funname] = {}
                functions[funname][signature] = f
    for funname, x in functions.items():
        is_distribution = funname[:-4] in distributions
        for sig in x:
            functions[funname][sig]['distribution'] = is_distribution
    return (functions, distributions)

def build(file_functions, file_keywords, dst):
    print("functions file: %s" % file_functions)
    with open(file_keywords, 'r') as f:
        data = yaml.load(f)
    functions, distributions = parse_functions(file_functions, data)
    version = re.search(r"-([0-9]+\.[0.9]+\.[0-9]+)\.txt$", file_functions).group(1)
    print("Stan version: %s" % version)
    data['version'] = version
    data['functions'] = functions
    data['distributions'] = list(sorted(distributions))
    constants = set()
    for funname, x in functions.items():
        if sum(len(functions[funname][sig]['args']) for sig in functions[funname]) == 0:
            constants.add(funname)
    data['constants'] = sorted(list(constants))
    data['operator_functions'] = ['operator%s' % x for x in data['operators']]
    with open(dst, 'w') as f:
        json.dump(data, f, sort_keys = True, indent = 2, separators = (',', ': '))

def main():
    dst = sys.argv[1]
    file_functions = glob.glob("stan/doc/stan-functions-*.txt")[0]
    file_keywords = 'stan-lang-keywords.yaml'
    build(file_functions, file_keywords, dst)

if __name__ == '__main__':
    main()
