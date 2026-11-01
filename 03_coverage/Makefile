.PHONY: install test unittest-cov pytest-cov coverage threshold html xml report clean

install:
	poetry install

test:
	poetry run pytest -v

unittest-cov:
	poetry run coverage erase && poetry run coverage run -m unittest discover && poetry run coverage report -m

pytest-cov:
	poetry run coverage erase && poetry run coverage run -m pytest && poetry run coverage report -m

coverage:
	poetry run pytest --cov=app --cov-branch --cov-report=term-missing -v

threshold:
	poetry run pytest --cov=app --cov-branch --cov-fail-under=90

html:
	poetry run coverage html

xml:
	poetry run coverage xml

report:
	py build_report.py

clean:
	rm -rf .pytest_cache .coverage htmlcov coverage.xml __pycache__
