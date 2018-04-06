
.PHONY: help clean rebuild test-all test

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  clean     to remove build artifacts."
	@echo "  rebuild   remove and recreate all tox virtual environments."
	@echo "  test-all  to run tests with all required python interpreters."
	@echo "  test      to run tests with every python interpreter available."

clean:
	@rm -fr 'dist/'
	@rm -fr 'build/'
	@rm -fr '.cache/'
	@rm -fr '.pytest_cache/'
	@find . -path '*/.*' -prune -o -name '__pycache__' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.egg-info' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.py[co]' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.build' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.so' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*.c' -exec rm -fr {} +
	@find . -path '*/.*' -prune -o -name '*~' -exec rm -fr {} +

rebuild:
	@make clean
	rm -fr .tox
	python -m tox --skip-missing-interpreters --recreate --notest
	@make clean


test-all:
	@make clean
	python -m tox
	@make clean

test:
	@make clean
	python -m tox --skip-missing-interpreters
	@make clean
