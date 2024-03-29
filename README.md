This is not literally the Stan Language definition, which is in the [Stan Modeling Language User's Guide and Reference Manual](http://mc-stan.org/documentation/).
This repo contains `stan-lang.json`, which contains various keywords and built-in functions in Stan that I use in maintaining several editor modes and syntax highlighting defintions.
In particular, this is used to generate the keyword and function lists in:

- Emacs [stan-mode](https://github.com/stan-dev/stan-mode) (Current maintainer: @kaz-yos).
- Atom [language-stan](https://github.com/jrnold/atom-language-stan).
- [Pygments](http://pygments.org/) StanLexer.
- LaTeX package [lstbayes](https://www.ctan.org/pkg/lstbayes) ([github](https://github.com/jrnold/lstbayes)).


## Updating this folder

`make all` in this directory invokes the `create_stan_lang.py` Python script. This script parses the following manually maintained files to construct the `stan-lang.json` file. `make clean` will delete this file.

- `stan-lang-keywords.yaml`
- `stan-functions-*.txt`

The `stan-functions-*.txt` file is generated by the `extract_function_sigs.py` script in the [stan docs repo](https://github.com/stan-dev/docs). For example, function signatures for Stan version 2.4.x can be generated as follows after cloning the stan-dev/docs repo.

```{sh}
git clone git@github.com:stan-dev/docs.git
cd docs
python3 extract_function_sigs.py
```

Copy the resulting file named `stan-functions-2_24.txt` to this repo.


## References

- [Stan Reference Manual, Version 2.24.0](https://mc-stan.org/docs/2_24/reference-manual/index.html)
  - [6 Expressions](https://mc-stan.org/docs/2_24/reference-manual/expressions.html)
  - [6.2 Variables](https://mc-stan.org/docs/2_24/reference-manual/variables-section.html)
  - [8.1 Overview of Stan’s Program Blocks](https://mc-stan.org/docs/2_24/reference-manual/overview-of-stans-program-blocks.html)
  - [11 Language Syntax](https://mc-stan.org/docs/2_24/reference-manual/language-syntax.html)
  - [13 Deprecated Features](https://mc-stan.org/docs/2_24/reference-manual/deprecated-features-appendix.html)


## Notes on Changes

### 2.28.1 (2021-11-03)
- Update functions to latest and parse new `array [] int` syntax as replacement for `int[]` syntax
- Add `.^` and `%/%` operators
- Add support for the `complex` type

###  2.24.x (2020-08-17)
- Explain function signature file generation using the extract_function_sigs.py script

###  2.22.0 (2020-02-12)

- Add `offset` and `multiplier` to keywords.

###  2.19.0 (2019-07-12)

- Links have been updated
- data only arguments in functions such as ODE functions are handled as special cases in the Python parsing script.

###  2.10.0

- `=` now used for assignment. `<-` is deprecated.
- New `target` keyword for `target += expression`
- Variable `lp__` is no longer supported
- Indicate `log_prob()` and `target()` as special functions
- Ternary operator `a ? b : c`
- New ODE integrate keywords: `integrate_ode`, `integrate_ode_rk45`, `integrate_ode_bdf` which support 6 or 9 arguments.
- Deprecate functions: `log_prob`, `increment_log_prob`, `binomial_log`, `multiply_log`
- `y ~ foo(a, b)` is deprecated in favor of `target += foo(y | a, b)`
- Distribution postfixes `_log`, `_cdf_log`, and `_ccdf_log` deprecated in favor of
  `_lpdf`, `_lpmf`, `_lcdf`, `_lccdf`, `_cdf`, `_ccdf`.
