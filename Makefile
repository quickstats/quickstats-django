APP_BIN := .venv/bin/quickstats
PIP_BIN := .venv/bin/pip

.PHONY:	test
test: ${APP_BIN}
	${APP_BIN} test -v 2

$(PIP_BIN):
	python3 -m venv .venv

${APP_BIN}: $(PIP_BIN)
	${PIP_BIN} install -r docker/requirements.txt
	${PIP_BIN} install -e .[dev,standalone]

.PHONY:	pip
pip:	$(PIP_BIN)
	${PIP_BIN} install -r docker/requirements.txt
	${PIP_BIN} install -e .[dev,standalone]

# Django and Python Commands

.PHONY:	migrate
migrate: ${APP_BIN}
	${APP_BIN} migrate
.PHONY:	run
run: migrate
	${APP_BIN} runserver
.PHONY: shell
shell: migrate
	${APP_BIN} shell
.PHONY: clean
clean:
	rm -rf .venv

# Docker and Release
.PHONY: build
build:
	docker-compose build 

.PHONY: release
release:	${PIP_BIN}
	${PYTHON_BIN} setup.py sdist
	twine check dist/*
