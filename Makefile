PYTHON ?= python3
STAN_LANG = stan_lang.json

all : json

json: $(STAN_LANG)

$(STAN_LANG) : create_stan_lang.py
	$(PYTHON) $< $@
