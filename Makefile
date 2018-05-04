.PHONY: test run clean

test: .env
	.env/bin/simplestats test

run: .env
	.env/bin/simplestats migrate
	.env/bin/simplestats runserver

.env:
	python3 -m venv .env
	.env/bin/pip install -e .[dev,standalone]

clean:
	rm -rf .env
