init:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	nosetests

.PHONY: test
