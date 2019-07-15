init:
	pip install pipenv
	pipenv install --dev
test:
	pipenv run pythton -m unittest