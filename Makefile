PYTHON ?= python
OUTPUT ?= build/generated

.PHONY: all
all:
	$(PYTHON) -m pyuml2.generation --output "$(OUTPUT)"
