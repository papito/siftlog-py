SHELL=/bin/sh

install:
	poetry install

lint:
	@poetry run isort siftlog/
	@poetry run black siftlog/
	@poetry run flake8
	@poetry run mypy siftlog/

test:
	@poetry run nosetests

info:
	@poetry env info
