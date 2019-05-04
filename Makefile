test:
	pipenv run simplestats test -v 2
migrate:
	pipenv run simplestats migrate
run: migrate
	pipenv run simplestats runserver

shell: migrate
	pipenv run simplestats shell

reset:
	pipenv run simplestats migrate simplestats zero
	git clean -f simplestats/migrations
	pipenv run simplestats makemigrations
	pipenv run simplestats migrate
