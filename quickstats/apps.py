from django.apps import AppConfig


class QuickstatsConfig(AppConfig):
    name = "quickstats"

    def ready(self):
        from . import signals  # NOQA
