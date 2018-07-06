"""Create regexes to match functions used in rstudio stan-mode."""
import json
import sys


_TEMPLATE = r"""
var functionList = "\\b({functions})\\b";

var distributionList = "(~)(\\s*)({distributions})\\b";

var deprecatedFunctionList = "\\b({deprecated_functions})\\b";

var reservedWords = "\\b({reserved})\\b";
"""


def clean_list(x):
    """Clean a list of documents."""
    return '|'.join(sorted(list(set(x))))

def read_json(filename):
    """Read and process json file of stan language dafinitions."""
    with open(filename, "r") as f:
        data = json.load(f)
    functions = [
        k for k, v in data['functions'].items()
        if not (v['operator'] or v['deprecated'] or v['keyword'])
    ]
    deprecated_functions = [
        k for k, v in data['functions'].items()
        if not v['operator'] and v['deprecated']
    ]
    distributions = [
        v['sampling'] for k, v in data['functions'].items()
        if v['sampling'] and not v['deprecated']
    ]
    reserved = data['reserved']['cpp'] + data['reserved']['stan']
    return {
        'functions': clean_list(functions),
        'distributions': clean_list(distributions),
        'deprecated_functions': clean_list(deprecated_functions),
        'reserved': clean_list(reserved)
    }


def main():
    """Command line interface."""
    data = read_json(sys.argv[1])
    print(_TEMPLATE.format(**data))


if __name__ == '__main__':
    main()
