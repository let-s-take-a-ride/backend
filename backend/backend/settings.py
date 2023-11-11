from pathlib import Path
import os
from configurations import Configuration, values
from dotenv import load_dotenv
import dj_database_url

import json
from six.moves.urllib import request
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
print(BASE_DIR)

class Dev(Configuration):


    SECRET_KEY = values.SecretValue()
    DEBUG = values.BooleanValue(True)
    AUTH0_DOMAIN = os.getenv('DJANGO_AUTH0_DOMAIN')
    AUTH0_AUDIENCE = os.getenv('DJANGO_AUTH0_AUDIENCE')
    AUTH0_ALGORITHMS = ['RS256']

    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:3000',
        "http://localhost:8000",
        'http://localhost:5173',
    ]

    SECURE_CROSS_ORIGIN_OPENER_POLICY = None

    INTERNAL_IPS = [
        '127.0.0.1',
        '192.168.0.100',
        'localhost',

    ]

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",
    ]

    INSTALLED_APPS = [
        'daphne',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # external modules

        'rest_framework',
        'debug_toolbar',
        'corsheaders',
        'rest_framework_swagger',
        'drf_yasg',
        'rest_framework_jwt',
        'rest_framework_simplejwt',
        'django_filters',
        'channels',
        'django_celery_results',
        'django_celery_beat',
        'celery',

        # app modules
        'core.apps.CoreConfig',
        'user.apps.UserConfig',
        'auth0authorization.apps.Auth0AuthorizationConfig',
        'workout.apps.WorkoutConfig',
        'notification.apps.NotificationConfig',

        # health check
        'health_check',
        'health_check.db',
        'health_check.cache',
        'health_check.storage',
        'health_check.contrib.migrations',
        'health_check.contrib.psutil'
    ]

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'corsheaders.middleware.CorsMiddleware',

        # 'core.auth_middleware.Auth0TokenMiddleware',

        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            # 'rest_framework.permissions.AllowAny',
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'auth0authorization.authentication.Auth0TokenAuthentication',
            'django.contrib.auth.backends.ModelBackend',
        ),
        'DEFAULT_THROTTLE_RATES': {
            'user': '1000/day',
            'anon': '100/day',
        },
    }

    # Celery
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # Celery
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

    CELERY_BROKER_CONNECTION_RETRY = True
    CELERY_BROKER_CONNECTION_MAX_RETRIES = 10

    CELERY_TIMEZONE = 'UTC'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60
    CELERYD_LOG_LEVEL = "INFO"  # or "DEBUG"

    # CELERY_RESULT_BACKEND = 'django-db'
    CELERY_CACHE_BACKEND = 'django-cache'

    CELERY_IMPORTS = ('core.tasks',)

    AUTH_USER_MODEL = 'user.CustomUser'

    ROOT_URLCONF = 'backend.urls'

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
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'backend.wsgi.application'
    ASGI_APPLICATION = 'backend.asgi.application'
    # ASGI_APPLICATION = 'routing.application'

    DATABASES = {
        'default': dj_database_url.config(),
        'alternative': dj_database_url.config(
            env="ALTERNATIVE_DATABASE_URL",
            default=f"sqlite:///alternative_db.sqlite3"
        )
    }

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

    # TIME_ZONE = 'UTC'
    TIME_ZONE = values.Value("UTC")

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = 'static/'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Prod(Dev):
    DEBUG = values.BooleanValue(False)
