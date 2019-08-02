This is not literally the Stan Language definition, which is in the [Stan Modeling Language User's Guide and Reference Manual](http://mc-stan.org/documentation/).
This repo contains `stan-lang.json`, which contains various keywords and built-in functions in Stan that I use in maintaining several editor modes and syntax highlighting defintions.
In particular, this is used to generate the keyword and function lists in:

- Emacs [stan-mode](https://github.com/stan-dev/stan-mode).
- Atom [language-stan](https://github.com/jrnold/atom-language-stan).
- [Pygments](http://pygments.org/) StanLexer.
- LaTeX package [lstbayes](https://www.ctan.org/pkg/lstbayes) ([github](https://github.com/jrnold/lstbayes)).


## Updating this folder

`make all` in this directory invokes the `create_stan_lang.py` Python script. This script parses the following manually maintained files to construct the `stan-lang.json` file. `make clean` will delete this file.

- `stan-lang-keywords.yaml`
- `stan-functions-*.txt`

The `stan-functions-*.txt` file is available as `stan-functions.txt` in the [rstan repo](https://github.com/stan-dev/rstan/blob/develop/rstan/rstan/tools/stan-functions.txt). Several errors have been addressed. Note that the name must contain the version string, for example, `stan-functions-2.19.0.txt`. Some scripts use this version string to record the current version.


## References

- [Stan Reference Manual, Version 2.19.0](https://mc-stan.org/docs/2_19/reference-manual/index.html)

    - [Chapter 6. Expressions](https://mc-stan.org/docs/2_19/reference-manual/expressions.html)
    - [Chapter 11. Language Syntax](https://mc-stan.org/docs/2_19/reference-manual/language-syntax.html)
    - [Chapter 13. Deprecated Features](https://mc-stan.org/docs/2_19/reference-manual/deprecated-features-appendix.html)


## Notes on Changes
###  2.19.0

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
