# 6.5 Setting Variables
# https://www.gnu.org/software/make/manual/html_node/Setting.html
# Variables defined with ‘=’ are recursively expanded variables.
# If you’d like a variable to be set to a value only if it’s not
# already set, then you can use the shorthand operator ‘?=’ instead
# of ‘=’.
# Variables defined with ‘:=’ or ‘::=’ are simply expanded variables.
# Use the python3 that has the pyyaml library installed.
# If doing conda install pyyaml, the conda python3 should be specified.
# Check with which -a python3 to see the priority.
# https://github.com/yaml/pyyaml/issues/291
PYTHON ?= ~/miniconda3/bin/python3
STAN_LANG_JSON = stan_lang.json
# This file must have a version string at * to ensure auto-retrieval.
FUNCTIONS_FILE := $(wildcard stan-functions-*.txt)

all : json

clean : clean-json


json : $(STAN_LANG_JSON)

clean-json :
	rm -rf $(STAN_LANG_JSON)


# Update in any one of
#  create_stan_lang.py (script)
#  stan-lang-keywords.yaml (hardcoded in the script)
#  stan-functions-*.txt (argument to the script)
# should invoke the recipe.
#
# Avoided "Automatic Variables" for readability.
# http://www.gnu.org/software/make/manual/make.html#Automatic-Variables
$(STAN_LANG_JSON) : create_stan_lang.py stan-lang-keywords.yaml $(FUNCTIONS_FILE)
	$(PYTHON) create_stan_lang.py $(STAN_LANG_JSON)

# mamba and expects were installed via conda's pip.
test :
	mamba specs_create_stan_lang.py
