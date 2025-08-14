### config/settings/prod.py

from .base import *

# Production-specific settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS Whitelist
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# Email Backend (using Anymail with a provider like SendGrid or Postmark)
# INSTALLED_APPS.append('anymail')
# EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
# ANYMAIL = {
#     "SENDGRID_API_KEY": env('SENDGRID_API_KEY'),
# }

# Static & Media Files (AWS S3)
# ------------------------------------------------------------------------------
# INSTALLED_APPS.append('storages')
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_DEFAULT_ACL = 'public-read'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Sentry & OpenTelemetry for Observability
# ------------------------------------------------------------------------------
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.redis import RedisIntegration
#
# sentry_sdk.init(
#     dsn=env('SENTRY_DSN'),
#     integrations=[
#         DjangoIntegration(),
#         CeleryIntegration(),
#         RedisIntegration(),
#     ],
#     traces_sample_rate=0.2, # Sample 20% of transactions
#     profiles_sample_rate=0.2,
#     send_default_pii=True
# )
