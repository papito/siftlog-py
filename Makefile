SHELL=/bin/sh

install:
	poetry install

build:
	poetry run mdToRst README.md > README.rst
	poetry build

lint:
	@poetry run isort siftlog/
	@poetry run black siftlog/
	@poetry run flake8
	@poetry run mypy siftlog/

test:
	@poetry run nosetests

info:
	@poetry env info
