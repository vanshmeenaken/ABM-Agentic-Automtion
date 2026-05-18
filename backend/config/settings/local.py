"""
Local development Django settings for Ken ABM Platform.
Extends base.py with development-specific overrides.
"""

from .base import *
import os

# SECURITY WARNING: never use these settings in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "django-api"]

# Database (use environment variables or defaults for local development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "ken_abm"),
        "USER": os.getenv("POSTGRES_USER", "ken_abm_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "localpassword"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# CORS — allow all origins in local development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for local development (outputs to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache — use dummy cache in local development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Logging — verbose output in local development
LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# Security settings (relaxed for local development)
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# REST Framework — lenient throttling for development
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []

# Celery — use eager mode for synchronous task execution in development (optional)
# Uncomment to run tasks synchronously instead of async
# CELERY_TASK_ALWAYS_EAGER = True
