### config/settings/dev.py

import socket

from .base import *  # noqa: F403
from .base import env

# Development-specific settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "django-app"]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Install Django Debug Toolbar
INSTALLED_APPS.append("debug_toolbar")  # noqa: F405
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# Allow debug toolbar to show for Docker container requests

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"] + [ip[:-1] + "1" for ip in ips]

# Use console for emails
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug Toolbar Configuration
DEBUG_TOOLBAR_CONFIG = {
    "ROOT_TAG_EXTRA_ATTRS": "data-turbo-permanent",
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}
