import environ

# Initialize django-environ
env = environ.Env(
    ENVIRONMENT=(str, "development"),
)

# Read .env file if it exists
environ.Env.read_env()

# Determine which settings to load based on ENVIRONMENT variable
if env("ENVIRONMENT") == "production":
    from .production import *  # noqa: F403
else:
    from .dev import *  # noqa: F403
