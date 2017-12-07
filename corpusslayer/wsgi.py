"""
WSGI config for corpusslayer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

if sys.version_info.major < 3:
    raise RuntimeError("Python %s is too old. Run with Python 3 or newer."%(sys.version.split()[0]))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corpusslayer.settings")

application = get_wsgi_application()
