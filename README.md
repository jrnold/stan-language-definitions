This is not literally the Stan Language definition, which is in the [Stan Modeling Language User's Guide and Reference Manual](http://mc-stan.org/documentation/).
This repo contains `stan-lang.json`, which contains various keywords and built-in functions in Stan that I use in maintaining several editor modes and syntax highlighting defintions.
In particular, this is used to generate the keyword and function lists in:

- Emacs [stan-mode](https://github.com/stan-dev/stan-mode).
- Atom [language-stan](https://github.com/jrnold/atom-language-stan).
- [Pygments](http://pygments.org/) StanLexer.
- LaTeX package [lstbayes](https://www.ctan.org/pkg/lstbayes) ([github](https://github.com/jrnold/lstbayes)).


## References

- [Modeling Language User's Guide and Reference Manual, Version 2.10.0](https://github.com/stan-dev/stan/releases/download/v2.10.0/stan-reference-2.10.0.pdf)

    - Chapter 30. Modeling Language Syntax.
    - Appendix E. Deprecated Features
    - Chapter 26. Expressions

## Notes on Changes

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
