.PHONY: init check format test coverage htmlcov requirements

init:
	pip install pipenv
	pipenv sync --dev

format:
	isort -rc -y avengers tests
	black -S -l 79 avengers tests

test:
	python -m pytest

coverage:
	python -m pytest --cov avengers --cov-report term --cov-report xml

htmlcov:
	python -m pytest --cov avengers --cov-report html
	rm -rf /tmp/htmlcov && mv htmlcov /tmp/
	open /tmp/htmlcov/index.html

requirements:
	pipenv lock -r > requirements.txt
	pipenv lock -dr > requirements-dev.txt
