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
    argtext = re.sub("[()]", "", argtext).strip()
    if argtext == "":
        ret = []
    elif argtext == "~":
        ret = None
    else:
        ret = []
        # , separates args, but they can appear within brackets like int[,]
        for arg in re.split(',(?!\\s*])', argtext):
            arg = arg.strip()
            if arg == '...':
                ret.append({'type': '...', 'name': '...'})
            else:
                argtype, argname = arg.split(' ')
                ret.append({'type': argtype.strip(),
                            'name': argname.strip()})
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
            # Ignore target +=
            if funname == 'target +=':
                continue
            else:
                args = parse_args(funargs)
                f = {
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
                              'keyword': funname in data['keywords']['functions']
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
