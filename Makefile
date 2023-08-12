lint:
	poetry run pysen run lint

format:
	poetry run pysen run format

test:
	pipenv run python -m unittest
