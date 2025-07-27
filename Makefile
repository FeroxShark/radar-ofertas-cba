.PHONY: dev test

dev:
pip install -r requirements.txt

test:
flake8
pytest -q
