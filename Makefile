PROJECT_NAME=vedro_pw

.PHONY: install
install:
	pip3 install --quiet --upgrade pip
	pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: build
build:
	pip3 install --quiet --upgrade pip
	pip3 install --quiet --upgrade setuptools wheel twine
	python3 setup.py sdist bdist_wheel

.PHONY: publish
publish:
	twine upload dist/*

.PHONY: test
test:
	python3 -m vedro run tests/

.PHONY: coverage
coverage:
	python3 -m coverage erase
	python3 -m coverage run -a -m vedro run tests/
	python3 -m coverage report
	python3 -m coverage xml -o $(or $(COV_REPORT_DEST),coverage.xml)

.PHONY: check-types
check-types:
	python3 -m mypy ${PROJECT_NAME} --strict

.PHONY: check-imports
check-imports:
	python3 -m isort ${PROJECT_NAME} tests --check-only

.PHONY: sort-imports
sort-imports:
	python3 -m isort ${PROJECT_NAME} tests

.PHONY: check-style
check-style:
	python3 -m flake8 ${PROJECT_NAME} tests

.PHONY: lint
lint: check-types check-style check-imports

.PHONY: all
all: install lint test

.PHONY: bump
bump:
	bump2version $(filter-out $@,$(MAKECMDGOALS))
	@git --no-pager show HEAD
	@echo
	@git verify-commit HEAD
	@git verify-tag `git describe`
	@echo
	# git push origin main --tags
%:
	@:
