test:
	pipenv run quickstats test -v 2
build:
	docker-compose build
migrate:
	pipenv run quickstats migrate
run: migrate
	pipenv run quickstats runserver

shell: migrate
	pipenv run quickstats shell

reset:
	pipenv run quickstats migrate quickstats zero
	git clean -f quickstats/migrations
	pipenv run quickstats makemigrations
	pipenv run quickstats migrate
