test:
	pipenv run python -m simplestats.standalone.manage test

run:
	pipenv run python -m simplestats.standalone.manage runserver

migrate:
	pipenv run python -m simplestats.standalone.manage migrate
