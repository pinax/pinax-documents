import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.documents"
    verbose_name = _("Pinax Documents")

    def ready(self):
        importlib.import_module("pinax.documents.receivers")
