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
                signature = ','.join(x['type'] for x in f['args'])
                if funname not in functions:
                    functions[funname] = {}
                    ## Add deprecated names for distributions
                    if re.match(r'.*_lcdf$', funname):
                        functions[re.sub(r'_lcdf$', '_cdf_log', funname)] = {'deprecated': True}
                    elif re.match(r'.*_lp[dm]f$', funname):
                        functions[re.sub(r'_lp[dm]f$', '_log', funname)] = {'deprecated': True}
                    elif re.match(r'.*_lccdf$', funname):
                        functions[re.sub(r'_lccdf$', '_ccdf_log', funname)] = {'deprecated': True}
                    elif funname in data['functions']['names']['deprecated']:
                        functions[funname]['deprecated'] = True
                    else:
                        functions[funname]['deprecated'] = False
                functions[funname][signature] = f
                ## Add deprecated names for distributions
                if re.match(r'.*_lcdf$', funname):
                    functions[re.sub(r'_lcdf$', '_cdf_log', funname)] = f
                if re.match(r'.*_lp[dm]f$', funname):
                    functions[re.sub(r'_lp[dm]f$', '_log', funname)] = f
                if re.match(r'.*_lccdf$', funname):
                    functions[re.sub(r'_lccdf$', '_ccdf_log', funname)] = f
    return functions

def build(file_functions, file_keywords, dst):
    print("functions file: %s" % file_functions)
    with open(file_keywords, 'r') as f:
        data = yaml.load(f)
    functions = parse_functions(file_functions, data)
    version = re.search(r"-([0-9]+\.[0-9]+\.[0-9]+)\.txt$", file_functions).group(1)
    print("Stan version: %s" % version)
    data['version'] = version

    data['functions']['signatures'] = functions
    data['functions']['names']['operators'] = sorted(['operator%s' % x for x in data['operators']])
    data['functions']['names']['all'] = sorted([x for x in data['functions']['signatures']
                                                if x not in data['functions']['names']['operators']])
    data['functions']['names']['density'] = sorted([x for x in data['functions']['signatures']
                                                    if re.match(r'.*_lp[dm]f$', x)])
    data['functions']['names']['lccdf'] = sorted([x for x in data['functions']['signatures']
                                                 if re.match(r'.*_lccdf$', x)])
    data['functions']['names']['lcdf'] = sorted([x for x in data['functions']['signatures']
                                                 if re.match(r'.*_lcdf$', x)])
    data['functions']['names']['rng'] = sorted([x for x in data['functions']['signatures']
                                                if re.match(r'.*_rng$', x)])
    data['functions']['names']['math'] = []
    for x in sorted(data['functions']['names']['all']):
        if x not in data['functions']['names']['density'] and \
           x not in data['functions']['names']['lccdf'] and \
           x not in data['functions']['names']['lcdf'] and \
           x not in data['functions']['names']['rng']:
            data['functions']['names']['math'].append(x)

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
