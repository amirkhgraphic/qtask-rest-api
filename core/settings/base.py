from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'pairs.apps.PairsConfig',

    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    # JWT Authentication configuration
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Invalid data label
    'NON_FIELD_ERRORS_KEY': 'invalid data',

    # Pagination Configuration
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomCursorPagination',
    'PAGE_SIZE': 20,

    # OpenAPI 3 documentation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': Path('keys/private.pem').read_text(),
    'VERIFYING_KEY': Path('keys/public.pem').read_text(),
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Key-Value REST API',
    'DESCRIPTION': (
        "This Key-Value REST API offers secure and efficient data management, "
        "featuring a flexible key-value storage system that supports both simple "
        "and nested pairs. Built with Django and Django REST Framework, the API "
        "is secured using JWT authentication with RS256 encryption, ensuring "
        "privacy and data integrity. Key features include:\n\n"
        "- **User Authentication**: Secure JWT-based user authentication for "
        "access control.\n"
        "- **Key-Value Storage**: Flexible handling of key-value data, supporting "
        "both flat and nested structures.\n"
        "- **Cursor Pagination**: Efficiently handles large data sets, improving "
        "client performance.\n"
        "- **Database Optimization**: PostgreSQL-backed with advanced indexing "
        "for optimized querying.\n"
        "- **Comprehensive Documentation**: OpenAPI 3 schema for easy integration.\n"
        "- **Testing and Coverage**: Ensures reliability and maintainability with "
        "automated tests and coverage reports.\n\n"
        "Built for production, this API is well-suited for high-traffic applications "
        "requiring secure, scalable, and reliable data storage."
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}
