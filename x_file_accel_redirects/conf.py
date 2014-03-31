# -*- coding: utf-8 -*-
from django.conf import settings

settings.X_FILE_ACCEL = getattr(settings, 'X_FILE_ACCEL', False)
