"""
Create regexes to match functions used in rstudio stan-mode
"""
import json
import re
import sys
from datetime import date

import jinja2
_TEMPLATE = """
var functionList = "{functions}";

var distributionList = "{distributions}";

var deprecatedFunctionList = "{deprecated_functions}";
"""



def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    functions = sorted([k for k, v in data['functions'].items()
                        if (not v['operator'] and not v['deprecated'])])
    deprecated_functions = sorted([k for k, v in data['functions'].items()
                        if not v['operator'] and v['deprecated']])
    distributions = sorted([v['sampling'] for k, v in data['functions'].items()
                            if v['sampling']])
    return {
        'functions': '|'.join(functions),
        'distributions': '|'.join(distributions),
        'deprecated_functions': '|'.join(deprecated_functions)
    }

def main():
    data = read_json(sys.argv[1])
    print(_TEMPLATE.format(**data))

if __name__ == '__main__':
    main()
