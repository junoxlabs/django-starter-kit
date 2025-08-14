### config/settings/dev.py

from .base import *

# Development-specific settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Install Django Debug Toolbar
INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]

# Use console for emails
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
