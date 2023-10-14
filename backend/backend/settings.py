from pathlib import Path
import os
from configurations import Configuration, values
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
print(BASE_DIR)

class Dev(Configuration):

    SECRET_KEY = values.SecretValue()
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue(["localhost", "127.0.0.1", "0.0.0.0"])


    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        #external modules
        'rest_framework',
        'debug_toolbar',
        'corsheaders',
        'rest_framework_swagger',
        'drf_yasg',

        #app modules
        'core',

        #health check
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
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

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

