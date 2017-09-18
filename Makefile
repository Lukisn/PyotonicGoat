.PHONY: help test coverage

help:
	# test        run unit test with automatic test discovery
	# coverage    check unit test code coverage

test:
	python -m unittest discover .

coverage:
	coverage run -m unittest discover .
	coverage report
	coverage html