
test:
	pipenv run simplestats test
.PHONY:	test

setup:
	pipenv install --dev
.PHONY:	setup

run:
	pipenv run simplestats migrate
	pipenv run simplestats runserver
.PHONY:	run
