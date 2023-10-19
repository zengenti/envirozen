# Consistent set of make tasks.
.DEFAULT_GOAL:= help  # because it's is a safe task.

clean:  # Remove all build, test, coverage and Python artifacts.
	rm -rf .venv
	find . -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

compile:  # Compile the requirements files using pip-tools.
	rm -f requirements.*
	.venv/bin/pip-compile --output-file=requirements.txt && echo "-e ." >> requirements.txt

.PHONY: docs  # because there is a directory called docs.
docs:  # Build the mkdocs documentation.
	.venv/bin/python -m mkdocs build --clean

format:  # Format the code with black.
	.venv/bin/python -m black --config pyproject.toml .

.PHONY: help
help: # Show help for each of the makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

lint:  # Lint the code with ruff.
	.venv/bin/python -m ruff .

mypy:  # Type check the code with mypy.
	.venv/bin/python -m mypy .

report:  # Report the python version and pip list.
	.venv/bin/python --version
	.venv/bin/python -m pip list -v

venv:  # Install the requirements for Python.
	-pyenv update
	-pyenv install --skip-existing
	python -m venv .venv
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip setuptools
	.venv/bin/python -m pip install -r requirements.txt

test:  # Run the unit tests.
	.venv/bin/python -m pytest ./tests