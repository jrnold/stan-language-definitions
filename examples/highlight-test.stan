/*
A file for testing Stan syntax highlighting.

This model is nonsensical, but it will parse correctly (albeit with deprecation warnings),
if the invalid sections are commented out.
*/
# also a comment
// also a comment
functions {
  void f1() {
    print("Hello world!");
  }
  real f2() {
    return 1.0;
  }
  int f3() {
    return 1;
  }
  vector f4() {
    return rep_vector(0.0, 3);
  }
  row_vector f5() {
    return rep_row_vector(0.0, 3);
  }
  matrix f6() {
    return rep_matrix(0.0, 2, 2);
  }
  real[] f7() {
    return rep_array(0.0, 1);
  }
  real[,] f8() {
    return rep_array(0.0, 1, 1);
  }
  real[,,] f9() {
    return rep_array(0.0, 1, 1, 1);
  }
  void f10(real alpha, int bravo, vector charlie, row_vector delta,
          matrix echo, real[] foxtrot, real[,] golf, real[,,] hotel) {
            print("Hello, world!");
          }
  real f11(real a, real b, real c) {
    return a + b + c;
  }
  // ode function
  real[] sho(real t,
              real[] y,
              real[] theta,
              real[] x_r,
              int[] x_i) {
    real dydt[2];
    dydt[1] = y[2];
    dydt[2] = -y[1] - theta[1] * y[2];
    return dydt;
  }
  /* INVALID START
  cov_matrix fbad() {
    return diag_matrix(rep_vector(1.0, 2));
  }
  void fbad2(cov_matrix a) {
  }
  vector sum(vector a) {
    return 1.0;
  }
  INVALID END */
}
data {
  int n;
  real y;
  
  // valid names
  real abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_abc;
  real a;
  real a3;
  real Sigma;
  real my_cpp_style_variable;
  real myCamelCaseVariable;
  // invalid names
  /* INVALID START
  int a__;
  int 1a;
  int _a
  int _;
  // C++ reserved
  real public;
  // Stan reserved
  real var;
  real fvar;
  real STAN_MAJOR;
  real true;
  real false;
  INVALID END */

  // all types should be highlighed
  int alpha;
  real bravo;
  vector[1] charlie;
  ordered[1] delta;
  positive_ordered[3] echo;
  simplex[1] foxtrot;
  row_vector[1] golf;
  matrix[1, 1] hotel;
  corr_matrix[3] india;
  cov_matrix[3] juliette;
  cholesky_factor_cov[3] kilo;
  cholesky_factor_corr[3] lima;

  // ranges;
  real<lower=0> november;
  real<upper=0> oscar;
  real<lower=-1,upper=1> mike;

  // arrays
  real papa[1];
  real quebec[1, 1];
  real romeo[1, 1, 1];

  // names beginning with keywords
  real iffffff;
  real whilest;
  // name ending with truncation
  real fooT;
  // ode stuff
  int<lower=1> T;
  real y0[2];
  real t0;
  real ts[T];
  real theta[1];
  real abs_tol;
  real rel_tol;
  int max_num_steps;
}
transformed data {
  real sierra;
  // ode stuff
  real x_r[0];
  int x_i[0];

  sierra = 1 + 1;
}
parameters {
  real tango;
}
transformed parameters {
  real uniform;
  uniform = 1 / tango;
}
model {
  real foo;
  int bar;
  real baz;
  // used in ODE
  real y_hat[T,2];

  ## Assignment Operators
  foo = 1.0;
  foo = 0.0;

  // valid integer literals
  bar = 0;
  bar = 1;
  bar = -1;
  bar = 256;
  bar = -127098;
  // valid real literals
  foo = 0.0;
  foo = 1.0;
  foo = 3.14;
  foo = -217.9387;
  foo = 0.123;
  foo = .123;
  foo = 1.;
  foo = -0.123;
  foo = -.123;
  foo = -1.;
  foo = 12e34;
  foo = 12E34;
  foo = 12.e34;
  foo = 12.E34;
  foo = 12.0e34;
  foo = 12.0E34;
  foo = .1e34;
  foo = .1E34;
  foo = -12e34;
  foo = -12E34;
  foo = -12.e34;
  foo = -12.E34;
  foo = -12.0e34;
  foo = -12.0E34;
  foo = -.1e34;
  foo = -.1E34;
  foo = 12e-34;
  foo = 12E-34;
  foo = 12.e-34;
  foo = 12.E-34;
  foo = 12.0e-34;
  foo = 12.0E-34;
  foo = .1e-34;
  foo = .1E-34;
  foo = -12e-34;
  foo = -12E-34;
  foo = -12.e-34;
  foo = -12.E-34;
  foo = -12.0e-34;
  foo = -12.0E-34;
  foo = -.1e-34;
  foo = -.1E-34;

  // constants and nullary functions
  foo = machine_precision();
  foo = pi();
  foo = e();
  foo = sqrt2();
  foo = log2();
  foo = log10();
  // special values
  foo = not_a_number();
  foo = positive_infinity();
  foo = negative_infinity();
  foo = machine_precision();
  // log probability
  foo = target();

  // functions
  foo = log(10);
  foo = exp(20);

  // target +=
  target += 0.0;
  // bug in parser right now. uncomment when fixed.
  // target += normal_lpdf(y, 0.0, 1.0)
  y ~ normal(0.0, 1.0);

  // distribution functions
  foo = normal_lpdf(0.5 | 0.0, 1.0);
  foo = normal_cdf(0.5, 0.0, 1.0);
  foo = normal_lcdf(0.5 | 0.0, 1.0);
  foo = normal_lccdf(0.5 | 0.0, 1.0);

  // truncation
  alpha ~ normal(0, 1) T[-0.5, 0.5];

  // highlighting non-built in functions
  f1();
  foo = f11(foo, 0.0, 1.0);

  // control structures
  for (i in 1:10) {
  }
  while (foo < 5.0) {
  }
  if (foo > 0) {
  } else if (foo < 0) {
  } else {
  }

  // operators
  bar = foo || foo;
  bar = foo && foo;
  bar = foo == foo;
  bar = foo != foo;
  bar = foo < foo;
  bar = foo <= foo;
  bar = foo > foo;
  bar = foo >= foo;
  foo = foo + foo;
  foo = foo - foo;
  foo = foo * foo;
  foo = foo / foo;
  foo = bar % bar;
  foo = foo .* foo;
  foo = foo ./ foo;
  bar = ! foo;
  foo = - foo;
  foo = + foo;
  foo = foo ^ 2.0;
  foo = foo ';
  bar = foo > 1 ? 0 : 1;

  // ODE Functions
  y_hat = integrate_ode_rk45(sho, y0, t0, ts, theta, x_r, x_i, rel_tol, abs_tol, max_num_steps);
  y_hat = integrate_ode_rk45(sho, y0, t0, ts, theta, x_r, x_i);
  y_hat = integrate_ode_bdf(sho, y0, t0, ts, theta, x_r, x_i, rel_tol, abs_tol, max_num_steps);
  y_hat = integrate_ode_bdf(sho, y0, t0, ts, theta, x_r, x_i);

  // print and reject statements
  print("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_~@#$%^&*`'-+={}[].,;: ");
  // should be an error with the backslash and " and tab
  /* INVALID START
  // print("\  ");
  INVALID END */
  print("
  ");
  print("Hello, world!");
  print("");
  reject("rejected!");

  // lp__ should be an error
  /* INVALID START
  lp__ = lp__ + 0.0;
  INVALID END */
  // Deprecated features
  // DEPRECATED START
  foo <- 1;
  increment_log_prob(0.0);
  y_hat = integrate_ode(sho, y0, t0, ts, theta, x_r, x_i);
  foo = get_lp();
  foo = multiply_log(1.0, 1.0);
  foo = binomial_coefficient_log(1.0, 1.0);
  // deprecated distribution functions versions
  foo = normal_log(0.5, 0.0, 1.0);
  foo = normal_cdf_log(0.5, 0.0, 1.0);
  foo = normal_ccdf_log(0.5, 0.0, 1.0);
  // DEPRECATED END
}
generated quantities {
  real baz;
  // sampling function
  baz = normal_rng(0.0, 1.0);
}
