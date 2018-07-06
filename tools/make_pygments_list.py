#!/usr/bin/env python
"""
Create the file _stan_builtins.py used in the `pygments` package from `stan_lang.json`.
"""
import json
import re
import sys
from datetime import date

import jinja2

_TEMPLATE = """# -*- coding: utf-8 -*-
\"\"\"
    pygments.lexers._stan_builtins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the names of functions for Stan used by
    ``pygments.lexers.math.StanLexer. This is for Stan language version {{version}}.

    :copyright: Copyright 2006-{{year}} by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
\"\"\"

KEYWORDS = (
{%- for kw in keywords|sort %}
    '{{ kw }}',
{%- endfor %}
)

TYPES = (
{%- for type in types|sort %}
    '{{ type }}',
{%- endfor %}
)

FUNCTIONS = (
{%- for fxn in functions|sort %}
    '{{ fxn }}',
{%- endfor %}
)

DISTRIBUTIONS = (
{%- for dist in distributions|sort %}
    '{{ dist }}',
{%- endfor %}
)

RESERVED = (
{%- for res in reserved|sort %}
    '{{ res }}',
{%- endfor %}
)
"""

def tostr(x):
    return [str(y) for y in x]

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    keywords = set()
    for k in data['keywords']:
        if k == "range_constraints":
            continue
        for x in data['keywords'][k]:
            # handle target separately
            if x == "target":
                continue
            keywords.add(x)
    keywords = sorted(list(keywords))

    reserved = set()
    for k in data['reserved']:
        for x in data['reserved'][k]:
            reserved.add(x)
    reserved = sorted(list(reserved))

    types = set()
    for k in data['types']:
        for x in data['types'][k]:
            types.add(x)
    types = sorted(list(types))

    functions = sorted([k for k, v in data['functions'].items() if not v['operator']])
    distributions = sorted([v['sampling'] for k, v in data['functions'].items()
                            if v['sampling']])
    return {
        'distributions': distributions,
        'functions': functions,
        'keywords': keywords,
        'reserved': reserved,
        'types': types,
        'version': data['version'],
        'year': date.today().year,
    }

def create_code(data):
    template = jinja2.Template(_TEMPLATE)
    print(template.render(data))

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    create_code(data)
