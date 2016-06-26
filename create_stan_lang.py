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

    for row in fundata:
        funname, funargs, funret = row[:3]
        # Ignore sampling statements
        if funargs == "~":
            continue
        else:
            # Ignore special functions
            if funname in data['keywords']['functions']:
                continue
            elif funname == 'target +=':
                continue
            else:
                args = parse_args(funargs)
                f = {
                    'name': funname,
                    'return': funret,
                    'args': args,
                }
                if funname in functions:
                    functions[funname]['signatures'].append(f)
                else:
                    vals = {
                              'signatures': [f],
                              'deprecated': False,
                              'lpdf': bool(re.match(r'.*_lpdf$', funname)),
                              'lpmf': bool(re.match(r'.*_lpmf$', funname)),
                              'lcdf': bool(re.match(r'.*_lcdf$', funname)),
                              'lccdf': bool(re.match(r'.*_lccdf$', funname)),
                              'operator': funname in ['operator%s' % x for x in data['operators']],
                              'deprecated': funname in data['functions']['names']['deprecated'],
                            }
                    vals['density'] = vals['lpdf'] or vals['lpmf']
                    if vals['density']:
                        vals['sampling'] = re.sub(r'_l[pm]f$', '', funname)
                    else:
                        vals['sampling'] = None
                    vals['math'] = not (vals['lpdf'] or vals['lpmf'] or
                                      vals['lcdf'] or vals['lccdf'])
                    functions[funname] = vals
                    
                    if vals['density']:
                        v = vals.copy()
                        v['deprecated'] = True
                        functions[re.sub(r'_lcdf$', '_log', funname)] = v
                    elif vals['lcdf']:
                        v = vals.copy()
                        v['deprecated'] = True
                        functions[re.sub(r'_lcdf$', '_cdf_log', funname)] = v
                    elif vals['lccdf']:
                        v = vals.copy()
                        v['deprecated'] = True
                        functions[re.sub(r'_lcdf$', '_ccdf_log', funname)] = v

    return functions

def build(file_functions, file_keywords, dst):
    print("functions file: %s" % file_functions)
    with open(file_keywords, 'r') as f:
        data = yaml.load(f)
    functions = parse_functions(file_functions, data)
    version = re.search(r"-([0-9]+\.[0-9]+\.[0-9]+)\.txt$", file_functions).group(1)
    print("Stan version: %s" % version)
    data['version'] = version
    data['functions'] = functions
    with open(dst, 'w') as f:
        json.dump(data, f, sort_keys = True, indent = 2, separators = (',', ': '))

def main():
    dst = sys.argv[1]
    file_functions = glob.glob("stan-functions-*.txt")[0]
    print("Using file %s\n" % file_functions)
    file_keywords = 'stan-lang-keywords.yaml'
    build(file_functions, file_keywords, dst)

if __name__ == '__main__':
    main()
