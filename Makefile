.PHONY: install test run check
install:
	python -m pip install -r requirements-dev.txt
	python -m playwright install chromium
test:
	python -m pytest -q
check:
	python -m compileall -q falvorn
	python -m pytest -q
run:
	python -m falvorn
