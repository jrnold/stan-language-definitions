"""
Create regexes to match functions used in rstudio stan-mode
"""
import json
import re
import sys
from datetime import date

import jinja2
_TEMPLATE = r"""
var functionList = "\\b({functions})\\b)";

var distributionList = "\\b({distributions})\\b";

var deprecatedFunctionList = "\\b({deprecated_functions})\\b";

var reservedWords = "\\b({reserved})\\b"
"""



def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    functions = sorted([k for k, v in data['functions'].items()
                        if not (v['operator'] or v['deprecated'] or v['keyword'])])
    deprecated_functions = sorted([k for k, v in data['functions'].items()
                        if not v['operator'] and v['deprecated']])
    distributions = sorted([v['sampling'] for k, v in data['functions'].items()
                            if v['sampling']])
    reserved = sorted(list(set(data['reserved']['cpp'] + data['reserved']['stan'])))
    return {
        'functions': '|'.join(functions),
        'distributions': '|'.join(distributions),
        'deprecated_functions': '|'.join(deprecated_functions),
        'reserved': '|'.join(reserved)
    }

def main():
    data = read_json(sys.argv[1])
    print(_TEMPLATE.format(**data))

if __name__ == '__main__':
    main()
