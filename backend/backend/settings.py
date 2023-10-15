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
        'http://localhost:5173',
        'https://nine-keys-bake.loca.lt'
        'https://solid-adults-lose.loca.lt'
    ]
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None

    INTERNAL_IPS = [
        '127.0.0.1',
        '192.168.0.100',
        'localhost',
        'https://nine-keys-bake.loca.lt'
    ]

    CORS_ALLOWED_ORIGINS = [
        'https://solid-adults-lose.loca.lt'
    ]

    INSTALLED_APPS = [
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

        # app modules
        'core',
        'user',
        'auth0authorization',

        # health check
        'health_check',
        'health_check.db',
        'health_check.cache',
        'health_check.storage',
        'health_check.contrib.migrations',
        'health_check.contrib.psutil'
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'corsheaders.middleware.CorsMiddleware',

        'core.auth_middleware.Auth0TokenMiddleware',

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
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'auth0authorization.authentication.Auth0TokenAuthentication'
        )
    }

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

