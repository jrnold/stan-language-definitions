/*
A file for testing Stan syntax highlighting.

This is a completely invalid model, but is useful for testing syntax highlighting
*/
# also a comment
// also a comment
functions {
  void f1(void a, real b) {
    return 1 / a;
  }
  real f2(int a, vector b, real c) {
    return a + b + c;
  }
}
data {
  // valid names
  real abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_abc;
  real a;
  real a3;
  real Sigma;
  real my_cpp_style_variable;
  real myCamelCaseVariable;
  // invalid names
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
  real papa[1]
  real quebec[1, 1];
  real romeo[1][1];

  // names beginning with keywords
  real iffffff;
  real whilest;
  // name ending with truncation
  real fooT;
}
transformed data {
  real sierra;
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

  // constants
  foo = machine_precision();
  foo = e();

  // functions
  foo = log(10);
  foo = exp(20);

  // sampling distributions
  y ~ normal_log(alpha, beta);

  // distribution functions
  foo = normal_lpdf(y | alpha, beta);
  foo = normal_lcdf(y | alpha, beta);
  foo = normal_lccdf(y | alpha, beta);
  foo = normal_lpdf(y | alpha, beta);
  foo = normal_lcdf(y |alpha, beta);
  foo = normal_lccdf(y | alpha, beta);

  // sampling distribution notation
  target += normal(y | alpha, beta);
  // deprecated samling distribution notation.
  y ~ normal_log(alpha, beta);

  // truncation
  alpha ~ normal(0, 1) T[-0.5, 0.5];

  // control structures
  for (i in 1:10) {
    tmp = tmp + 1;
  }
  while (tmp < 5.0) {
    tmp = tmp + 1;
  }
  if (tmp > 0) {
    tmp = tmp + 1;
  } else if (tmp < 0) {
    tmp = tmp + 1;
  } else {
    tmp = tmp + 1;
  }

  // operators
  foo || foo;
  foo && foo;
  foo == foo;
  foo != foo;
  foo < foo;
  foo <= foo;
  foo > foo;
  foo >= foo;
  foo + foo;
  foo - foo;
  foo * foo;
  foo / foo;
  foo % foo;
  foo .* foo;
  foo ./ foo;
  ! foo;
  - foo;
  + foo;
  foo ^ foo;
  foo ';
  foo > 1 ? 0 : 1;

  // Incrementing log probability
  target += 0.0;

  // Accessing log-probability with and target()
  foo = target();

  // ODE
  y_hat = integrate_ode_rk45(sho, y0, t0, ts, theta, x_r, x_i, rel_tol, abs_tol, max_num_steps);
  y_hat = integrate_ode_bdf(sho, y0, t0, ts, theta, x_r, x_i, rel_tol, abs_tol, max_num_steps);

  // print and reject statements
  print("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_~@#$%^&*`'-+={}[].,;: ");
  // should be an error with the backslash and " and tab
  print("\  ");
  print("Hello, world!");
  print("");
  reject("rejected!");

  // lp__ should be an error
  lp__ = lp__ + 0.0;
  // Deprecated features
  foo <- 1;
  increment_log_prob(0.0);
  y_hat = integrate_ode(sho, y0, t0, ts, theta, x_r, x_i);
  get_lp()
  multiply_log()
  binomial_coefficient_log()
  // deprecated distribution functions versions
  foo = normal_log(y, alpha, beta);
  foo = normal_cdf(y, alpha, beta);
  foo = normal_cdf_log(y, alpha, beta);
  foo = normal_ccdf_log(y, alpha, beta);
}
generated quantities {
  real baz;
  // sampling
  baz = normal_rng(y, alpha, beta);
}
