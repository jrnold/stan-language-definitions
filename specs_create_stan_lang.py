
# https://github.com/nestorsalceda/mamba
from mamba import description, context, it
from expects import expect, equal

from create_stan_lang import *

with description("parse_args") as self:
    with it("parses empty argument correctly"):
        expect(parse_args("")).to(equal([]))
    #
    with it("parses ~ argument correctly regardless of spaces"):
        expect(parse_args("~")).to(equal(None))
        expect(parse_args("~ ")).to(equal(None))
        expect(parse_args("~  ")).to(equal(None))
        expect(parse_args(" ~")).to(equal(None))
        expect(parse_args("  ~")).to(equal(None))
        expect(parse_args(" ~ ")).to(equal(None))
    #
    with it("parses single argument into a single element list"):
        expect(parse_args("T x")).to(equal([{'type': 'T', 'name': 'x'}]))
        expect(parse_args("reals theta")).to(equal([{'type': 'reals', 'name': 'theta'}]))
    #
    with it("parses multiple arguments into a multi-element list"):
        expect(parse_args("T x, T y")
        ).to(equal([{'type': 'T', 'name': 'x'},
                    {'type': 'T', 'name': 'y'}]))
        expect(parse_args("matrix x, matrix y")
        ).to(equal([{'type': 'matrix', 'name': 'x'},
                    {'type': 'matrix', 'name': 'y'}]))
