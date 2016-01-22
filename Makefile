#!/bin/bash -e

CONFIG_FILE = config.json

all: install serve

serve: bootstrap
	@. venv/bin/activate; \
		echo "Starting Flask server..."; \
		python run.py

bootstrap:
	@. venv/bin/activate; \
		set -e; \
		echo "Bootstrapping app..."; \
		python bootstrap.py $(CONFIG_FILE) $(app_route); \

install: venv configure
	@. venv/bin/activate; \
		echo "Resolving Python dependencies..."; \
		pip install --upgrade -r requirements.txt

configure:
	@. venv/bin/activate; \
		python configure.py $(CONFIG_FILE)

venv:
	@ echo "Setting up virtual environment..."
	@ virtualenv venv

clean:
	@ echo "Deleting virtual environment..."
	@ rm -rf venv
	@ echo "Deleting configuration file..."
	@ rm -f $(CONFIG_FILE)
