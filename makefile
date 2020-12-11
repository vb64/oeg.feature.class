.PHONY: all setup tests
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = oeg_feature_class
TESTS = tests
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PIP = $(PYTHON) -m pip install

all: tests

test:
	$(PYTEST) -s --cov-append $(TESTS)/test/$(T)
	$(COVERAGE) html --skip-covered

tests: flake8 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

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

setup3: setup_python3 setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r tests/requirements.txt
	$(PIP) -r deploy.txt

setup_python3:
	$(PYTHON_BIN) -m venv ./venv

setup_python:
	$(PYTHON_BIN) -m virtualenv ./venv
