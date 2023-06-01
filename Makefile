# Formatting
format-black:
	@echo Formatting with black ...
	@black blenderline

format-isort:
	@echo.
	@echo Formatting with isort ...
	@isort blenderline

format-project: format-black format-isort

# Linting
lint-project:
	@echo Linting with flake8 ...
	@flake8 blenderline

# Building
build-project:
	@python setup.py bdist_wheel sdist

# Publishing
publish-project:
	@twine check dist/*
	@twine upload dist/*