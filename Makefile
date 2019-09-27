.PHONY: init check format test coverage htmlcov requirements

init:
	pip install pipenv
	pipenv sync --dev

format:
	isort -rc -y avengers tests
	black -S -l 79 avengers tests

test:
	python -m pytest --cov=./avengers ./tests


requirements:
	pipenv lock -r > requirements.txt
	pipenv lock -dr > requirements-dev.txt
