from django.conf import settings  # noqa

from appconf import AppConf


class DocumentsAppConf(AppConf):

    USE_X_ACCEL_REDIRECT = False
