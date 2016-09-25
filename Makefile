.PHONY: bootstrap
bootstrap:
	python simplestats/standalone/manage.py migrate
	python simplestats/standalone/manage.py createsuperuser
