.PHONY: insttall
install:
	python -m pip install --upgrade setuptools pip poetry
	python -m poetry install
	pre-commit install

.PHONY: pre-deploy
pre-deploy:
	python -m poetry export --output requirements.txt
