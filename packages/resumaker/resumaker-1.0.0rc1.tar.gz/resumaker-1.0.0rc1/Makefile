build:
	rm -rf dist/*
	hatch build
install:
	pip install --force-reinstall dist/resumaker*.whl
build-install:
	make build
	make install
fmt:
	black src/
	black tests/
lint:
	python -m flake8 src/
test:
	PYTHONPATH="$(shell pwd)/src:$$PYTHONPATH" pytest $(PTARGS)
test-cov:
	PYTHONPATH="$(shell pwd)/src:$$PYTHONPATH" pytest --cov=resumaker
