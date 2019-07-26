# 6.5 Setting Variables
# https://www.gnu.org/software/make/manual/html_node/Setting.html
# Variables defined with ‘=’ are recursively expanded variables.
# If you’d like a variable to be set to a value only if it’s not
# already set, then you can use the shorthand operator ‘?=’ instead
# of ‘=’.
# Variables defined with ‘:=’ or ‘::=’ are simply expanded variables.
PYTHON ?= python3
STAN_LANG_JSON = stan_lang.json
# This file must have a version string at * to ensure auto-retrieval.
FUNCTIONS_FILE := $(wildcard stan-functions-*.txt)

all : json

json: $(STAN_LANG_JSON)

# 10.5.3 Automatic Variables
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html
$(STAN_LANG_JSON) : $(FUNCTIONS_FILE) stan-lang-keywords.yaml
	$(PYTHON) create_stan_lang.py $(STAN_LANG_JSON)
