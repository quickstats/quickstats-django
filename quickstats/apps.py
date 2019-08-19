from django.apps import AppConfig


class quickstatsConfig(AppConfig):
    name = "quickstats"

    def ready(self):
        from . import signals  # NOQA
