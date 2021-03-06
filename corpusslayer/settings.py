"""
Django settings for corpusslayer project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

import os
import sys

proj_b_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_b_dir not in sys.path:
    sys.path.insert(0, proj_b_dir)
if proj_b_dir not in os.environ['PATH']:
    os.environ['PATH']+=':'+proj_b_dir
del proj_b_dir

from corpusslayer import fsconfig
from corpusslayer import fsplugin

SITE_NAME = fsconfig.SITE_NAME
BASE_DIR = fsconfig.BASE_DIR
SECRET_KEY = fsconfig.SECRET_KEY
DEBUG = fsconfig.DEBUG
ALLOWED_HOSTS = [
    fsconfig.SITE_DOMAIN,
    'localhost',
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_forms_bootstrap',
    'django_template_check',
    'django-dia',
    'rosetta',
    'ckeditor',
    'application',
    'view.api',
    'view.pages',
]

INSTALLED_APPS += list(fsplugin.enabledPlugins.keys())

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'corpusslayer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

TEMPLATES[0]['DIRS']+=fsplugin.enabledPluginsTemplatesDir
TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR,'templates'))

WSGI_APPLICATION = 'corpusslayer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGES = [(iso, _(lang)) for iso, lang in fsconfig.LANGUAGES]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    fsconfig.LNGS,
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
	os.path.join(BASE_DIR,'staticSource'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat']
        ]
    }
}

DEVELOPING = os.uname()[1] == 'forest'

if DEBUG and DEVELOPING:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = SITE_NAME+' <noreply@'+fsconfig.SITE_DOMAIN+'>'

from server_secrets.mailconfig import *

SETTINGS_EXPORT = [
    'SITE_NAME',
]

ROSETTA_WSGI_AUTO_RELOAD = True

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DEFAULT_FROM_EMAIL = SITE_NAME+' Registration <registration@'+fsconfig.SITE_DOMAIN+'>'
REGISTRATION_EMAIL_HTML = True
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_OPEN = fsconfig.REGISTRATION_OPEN
