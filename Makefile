PYTHON ?= python
STAN_LANG = stan_lang.json

all : json

stan-docs:
	-make -C stan docs

json: stan-docs $(STAN_LANG) 

$(STAN_LANG) : create_stan_lang.py
	$(PYTHON) $^ $@

.PHONY: stan-docs
