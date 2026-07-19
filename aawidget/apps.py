"""App Configuration"""

from django.apps import AppConfig

from aawidget import __version__


class AAWidgetConfig(AppConfig):
    name = "aawidget"
    label = "aawidget"
    verbose_name = f"Widget v{__version__}"
