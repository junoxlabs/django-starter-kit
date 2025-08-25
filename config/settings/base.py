### config/settings/base.py

import os
import re
from pathlib import Path
import environ
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from sentry_sdk.integrations.redis import RedisIntegration

# Initialize django-environ with default values
env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "development"),
    SECRET_KEY=(str, "django-insecure-development-key-for-local-use-only"),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, "postgresql://postgres:postgres@db:5432/db"),
    REDIS_URL=(str, "redis://redis:6379"),
    RABBITMQ_URL=(str, "amqp://guest:guest@rabbitmq:5672/"),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    POSTMARK_SERVER_TOKEN=(str, ""),
    SENTRY_DSN=(str, ""),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Core Settings
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Application definition
INSTALLED_APPS = [
    "django_dramatiq",
    # Local Apps
    "apps.core",
    "apps.users",
    "apps.api",
    "apps.pages",
    # Django Built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third Party
    "turbo_helper",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid_connect",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.microsoft",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_vite",
    "imagekit",
    "channels",
    "anymail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "turbo_helper.middleware.TurboMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Allauth
]

# Django REST Framework Settings
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL")],
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Authentication
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # For production 'collectstatic'
STATICFILES_DIRS = [
    BASE_DIR / "frontend/dist",  # Vite build output
]


# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_IMMUTABLE_FILE_TEST
def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

# Django-Vite Settings
# ------------------------------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": True if env("ENVIRONMENT") == "development" else False,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
    }
}

# Media files (User uploads)
# ------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# S3 Storage Settings
# ------------------------------------------------------------------------------
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
# STATIC_URL is already defined above, this is for S3 static files
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Override default storage for media files if AWS credentials are provided
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    STORAGES["default"]["BACKEND"] = "storages.backends.s3boto3.S3Boto3Storage"

# Email
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"

# Cache
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
# Dramatiq
# ------------------------------------------------------------------------------
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": env("RABBITMQ_URL"),
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ]
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled. The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"

# Anymail
# ------------------------------------------------------------------------------
ANYMAIL = {
    "POSTMARK_SERVER_TOKEN": env("POSTMARK_SERVER_TOKEN"),
}

# Sentry & OpenTelemetry
# ------------------------------------------------------------------------------

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# ImageKit
# ------------------------------------------------------------------------------
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
