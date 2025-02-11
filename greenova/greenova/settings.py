"""
Django settings for greenova project.

Generated by 'django-admin startproject' using Django 5.1.5.
"""

import logging  # noqa: F401 - Used in logging configuration
import mimetypes
import os
import sys
from pathlib import Path

# Validate required environment variables
required_env_vars = [
    "DJANGO_SECRET_KEY",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_TIME_ZONE",
    "GREENOVA_ENVIRONMENT",
    "GREENOVA_VERSION",
]

missing_vars = [var for var in required_env_vars if var not in os.environ]
if missing_vars:
    raise Exception(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-x#ycjskj0ixlnrs1^_*p7yifnlp*i)0ubz!cj89li@s7h=de9)",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)
mimetypes.add_type("text/html", ".html", True)
mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/webp", ".webp", True)

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
).split(",")

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# CSRF_TRUSTED_ORIGINS = [
#     "https://app.enssol.com.au",
#     "http://localhost:8000",
# ]

# HTTPS/SSL Settings
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "False") == "True"
# SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SESSION_COOKIE_SECURE", "False") == "True"
# CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", "False") == "True"

# Environment detection
ENVIRONMENT = os.environ.get("GREENOVA_ENVIRONMENT", "development")
VERSION = os.environ.get("GREENOVA_VERSION", "1.0.0")

# Environment-specific settings
if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    WHITENOISE_MANIFEST_STRICT = True
    WHITENOISE_ALLOW_ALL_ORIGINS = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "landing.apps.LandingConfig",
    "services.apps.ServicesConfig",
    "dashboard.apps.DashboardConfig",
    "obligations.apps.ObligationsConfig",
]

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard:index'  # Redirect after login
LOGOUT_REDIRECT_URL = 'landing:index'  # Redirect after logout

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "greenova.middleware.DashboardRedirectMiddleware",  # Add this line
]

# CORS Settings
CORS_ALLOWED_ORIGINS = ["https://app.enssol.com.au", "http://localhost:8000"]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "greenova.urls"

# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "accounts/templates",
            BASE_DIR / "core/templates",
            BASE_DIR / "dashboard/templates",
            BASE_DIR / "landing/templates",
            BASE_DIR / "services/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# ASGI_APPLICATION = "greenova.asgi.application"
WSGI_APPLICATION = "greenova.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": BASE_DIR / os.environ.get("DATABASE_NAME", "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-au"

TIME_ZONE = "Australia/Perth"

USE_I18N = True

USE_TZ = True

DEFAULT_CHARSET = "utf-8"

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)  # Create a dedicated directory for collected static files

# Extra static file locations
STATICFILES_DIRS = [BASE_DIR / "static"]

# Compression settings
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# Django Compressor settings
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ["compressor.filters.css_default.CssAbsoluteFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_ROOT = STATIC_ROOT

# WhiteNoise Configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# WhiteNoise Compression and Caching Settings
WHITENOISE_COMPRESSION_ENABLED = True
WHITENOISE_AUTOREFRESH = True  # Set to True only in development
WHITENOISE_USE_FINDERS = True  # Set to True only in development
WHITENOISE_MANIFEST_STRICT = False  # Set to True in production
WHITENOISE_ALLOW_ALL_ORIGINS = True  # Restrict in production

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Compression settings
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ["compressor.filters.css_default.CssAbsoluteFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]

# Security Headers
X_FRAME_OPTIONS = "DENY"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 1025))

# Email settings for password reset
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# LOGIN_REDIRECT_URL = "/"
# LOGOUT_REDIRECT_URL = "/"

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {message}", "style": "{"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",  # Change this to ERROR to suppress SQL logs
            "propagate": False,
        },
    },
}

# Override database logging in debug mode
if DEBUG and os.environ.get("DEV_SQL_PRINT", "False") == "True":
    LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"

# File upload settings
# FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('OBLIGATION_FILE_UPLOAD_MAX_SIZE',))
ALLOWED_UPLOAD_EXTENSIONS = os.environ.get(
    "OBLIGATION_ALLOWED_FILE_TYPES", ".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg"
).split(",")

# Cache settings
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": os.environ.get('CACHE_KEY_PREFIX', 'greenova'),
#         "TIMEOUT": int(os.environ.get('CACHE_TIMEOUT', 300)),
#     }
# }

# Custom app settings
OBLIGATIONS_SETTINGS = {
    "PER_PAGE": 20,
    "RECENT_ITEMS": 5,
    "WARNING_DAYS": 14,
    "CRITICAL_DAYS": 7,
    "AUTO_REMINDER_DAYS": int(
        os.environ.get("OBLIGATION_AUTO_REMINDER_DAYS", 14)
    ),
    "CRITICAL_THRESHOLD_DAYS": int(
        os.environ.get("OBLIGATION_CRITICAL_THRESHOLD_DAYS", 7)
    ),
    "EXPORT_FORMATS": os.environ.get(
        "OBLIGATION_EXPORT_FORMATS", "csv,xlsx,pdf"
    ).split(","),
}

AUDIT_SETTINGS = {
    "RETENTION_PERIOD": int(os.environ.get("AUDIT_RETENTION_PERIOD", 365)),
    "BATCH_SIZE": int(os.environ.get("AUDIT_BATCH_SIZE", 1000)),
    "EXPORT_FORMAT": os.environ.get("AUDIT_EXPORT_FORMAT", "csv"),
}

DASHBOARD_SETTINGS = {'STATS_REFRESH_INTERVAL': 30}  # seconds

# Add template caching in production
if not DEBUG:
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        )
    ]

# Test runner configuration
TEST_RUNNER = "django.test.runner.DiscoverRunner"

if "test" in sys.argv:
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
    }
