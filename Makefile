PIPENV := $(shell command -v pipenv 2> /dev/null)

.PHONY: install test clean release

ROOT_PATH=$(shell pwd)
KEY_FILE=tests/fixtures/privkey.pem

install:
ifndef PIPENV
	@echo "You must have pipenv installed (https://pipenv.kennethreitz.org/en/latest/)."
	@echo
	@exit 1
endif
	@pipenv install --dev

keygen: 
	@if [ ! -f "$KEY_FILE" ]; then openssl genrsa -out ${KEY_FILE} 4096 &>/dev/null; fi

test: keygen unit

qa:
	@pipenv run flake8

unit:
	@pipenv run pytest -s --cov

clean:
	-@rm -rf $(ROOT_PATH)/*.egg-info
	-@rm -rf $(ROOT_PATH)/dist
	-@rm -rf $(ROOT_PATH)/build

release: clean
	@pipenv run python setup.py sdist
	@pipenv run twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
