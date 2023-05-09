# Formatting
format-black:
	@echo Formatting with black ...
	@black blenderline

format-isort:
	@echo.
	@echo Formatting with isort ...
	@isort blenderline

format: format-black format-isort

# Linting
lint-flake8:
	@echo Linting with flake8 ...
	@flake8 blenderline

lint-mypy:
	@echo.
	@echo Linting with mypy ...
	@mypy blenderline

lint: lint-flake8 lint-mypy

# Build
build:
	@python setup.py bdist_wheel sdist