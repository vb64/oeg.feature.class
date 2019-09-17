.PHONY: all setup tests
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = oeg_feature_class
TESTS = tests
COVERAGE = $(PYTHON) -m coverage
PIP = $(PYTHON) -m pip install

all: tests

test:
	$(PYTHON) $(TESTS)/run_tests.py test.$(T)

html:
	$(COVERAGE) html --skip-covered

coverage:
	$(COVERAGE) run $(TESTS)/run_tests.py

tests: flake8 lint coverage html
	$(COVERAGE) report --skip-covered

verbose:
	$(PYTHON) $(TESTS)/run_tests.py verbose

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(TESTS)/test
	$(PYTHON) -m pylint $(SOURCE)

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r tests/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
