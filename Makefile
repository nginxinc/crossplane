
clean:
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.build' -exec rm -fr {} +
	@find . -name '*.so' -exec rm -fr {} +
	@find . -name '*.c' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -fr {} +
	@find . -name '*.pyo' -exec rm -fr {} +
	@find . -name '*~' -exec rm -fr {} +

test: clean
	python -m tox

