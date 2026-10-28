.PHONY: install dev test run docker
install:
	python -m pip install -r requirements.txt

dev:
	python -m falvorn

test:
	python -m pytest -q

docker:
	docker compose up --build
