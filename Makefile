test:
	pipenv run simplestats test -v 2

run:
	pipenv run simplestats migrate
	pipenv run simplestats runserver

reset:
	pipenv run simplestats migrate simplestats zero
	git clean -f simplestats/migrations
	pipenv run simplestats makemigrations
	pipenv run simplestats migrate
