# Format source code using black formatter
.PHONY: black
black:
	@echo Formatting with black ...
	@black blenderline

# Format source code using isort formatter
.PHONY: isort
isort:
	@echo Formatting with isort ...
	@isort blenderline

# Run both formatters
.PHONY: format
format: black isort

# Lint source code using flake8 linter
.PHONY: lint
lint:
	@echo Linting with flake8 ...
	@flake8 blenderline

# Build BlenderLine using setuptools
.PHONY: build
build:
	@echo Building with setuptools ...
	@python setup.py bdist_wheel sdist

# Publish BlenderLine to PyPI using twine (make sure to bump version beforehand)
.PHONY: publish
publish:
	@echo Checking package with twine ...
	@twine check dist/*
	@echo Uploading package with twine ...
	@twine upload dist/*

# Build BlenderLine documentation 
.PHONY: docs
docs:
	@echo Building documentation with sphinx ...
	@sphinx-build -b html -a -E -j=auto docs/source docs/build/html

# Build BlenderLine documentation with live test-server for development
.PHONY: livedocs
livedocs:
	@echo Starting development documentation server with sphinx-autobuild ...
	@sphinx-autobuild -b html -a -E -j=auto --watch blenderline docs/source docs/build/html
