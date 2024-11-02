from .base import *
from core.settings import env

import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

database_url = os.getenv("DATABASE_URL", default=None)
if database_url:
    DATABASES = {
        'default': dj_database_url.config(default=database_url)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE"),
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
