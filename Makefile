SHELL=/bin/sh

install:
	poetry install

build:
	poetry build

lint:
	@poetry run isort siftlog/
	@poetry run black siftlog/
	@poetry run flake8 siftlog/__init__.py siftlog/tests/
	@poetry run mypy siftlog/

test:
	@poetry run nosetests

visual:
	@poetry run nosetests -s

info:
	@poetry env info
