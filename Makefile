lint:
	poetry run pysen run lint

format:
	poetry run pysen run format

test:
	poetry run python -m unittest discover -v -s ./tests
