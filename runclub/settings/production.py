import os

import dj_database_url

from .base import *  # noqa: F401, F403

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Kommagescheiden lijst van hosts. Gebruik Django's dot-notatie voor subdomeinen:
#   .up.railway.app   → matcht alle *.up.railway.app subdomeinen
#   healthcheck.railway.app → Railway's interne healthcheck
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

# ── Database ──────────────────────────────────────────────────────────────────
# Railway injecteert automatisch DATABASE_URL (postgresql://user:pass@host/db)
DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ── Middleware ────────────────────────────────────────────────────────────────
# SecurityMiddleware eerst, WhiteNoise direct daarna voor static files
MIDDLEWARE = [  # noqa: F405
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# ── Storage ───────────────────────────────────────────────────────────────────
# Stel AWS_STORAGE_BUCKET_NAME in om S3-compatibele opslag te activeren
# (aanbevolen: Cloudflare R2 — gratis tot 10 GB, geen egress-kosten).
# Zonder deze variabele worden media-bestanden lokaal opgeslagen; ze
# verdwijnen dan bij elke Railway-redeploy.

_s3_bucket = os.environ.get("AWS_STORAGE_BUCKET_NAME")

if _s3_bucket:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": os.environ["AWS_ACCESS_KEY_ID"],
                "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"],
                "bucket_name": _s3_bucket,
                "endpoint_url": os.environ.get("AWS_S3_ENDPOINT_URL"),
                "custom_domain": os.environ.get("AWS_S3_CUSTOM_DOMAIN"),
                "file_overwrite": False,
                "querystring_auth": False,
                "default_acl": "public-read",
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    _custom_domain = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
    _endpoint = os.environ.get("AWS_S3_ENDPOINT_URL", "")
    MEDIA_URL = (
        f"https://{_custom_domain}/"
        if _custom_domain
        else f"{_endpoint}/{_s3_bucket}/"
    )
else:
    # Geen S3: lokale opslag + Django serveert /media/ zelf.
    # Bestanden zijn tijdelijk — gebruik S3 voor persistentie.
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

# ── Security ──────────────────────────────────────────────────────────────────
# Railway termineert SSL bij hun load balancer — de app ontvangt intern HTTP.
# SECURE_SSL_REDIRECT zou een redirect-loop veroorzaken; gebruik proxy-header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Railway-domein + eigen domein toestaan voor CSRF
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# ── E-mail ────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@runclub.example.com")

# ── Wagtail ───────────────────────────────────────────────────────────────────
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "https://runclub.example.com")

# ── Logging ───────────────────────────────────────────────────────────────────
# Stuur alle Django-fouten naar stderr zodat Railway ze opvangt in Deploy Logs.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
