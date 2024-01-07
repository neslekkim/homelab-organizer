"""
Django settings for hlo project.
"""
import os
import os.path
from pathlib import Path
from typing import List, Dict, Any
import environ  # type: ignore

env = environ.FileAwareEnv(
    # set casting, default value
    HLO_DEBUG=(bool, False),
    HLO_ALLOWED_HOSTS=(list, []),
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    HLO_LANGUAGE_CODE=(str, "nb"),
    HLO_TIME_ZONE=(str, "UTC"),
    HLO_USE_I18N=(bool, False),
    HLO_USE_L10N=(bool, False),
    HLO_USE_TZ=(bool, True),
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    HLO_STATIC_URL=(str, "/static/"),
    HLO_PASSWORD_MIN_LEN=(int, 14),
)

env.prefix = "HLO_"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

MEDIA_ROOT: Path = (BASE_DIR / Path("media_root")).resolve()
MEDIA_URL: str = "files/"
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG: bool = env("DEBUG")

INTERNAL_IPS = [
    "127.0.0.1"
]

LANGUAGE_CODE: str = env("LANGUAGE_CODE")
TIME_ZONE: str = env("TIME_ZONE")
USE_I18N: bool = env("USE_I18N")
USE_L10N: bool = env("USE_L10N")
USE_TZ: bool = env("USE_TZ")

DATE_FORMAT = 'Y-m-d'

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY: str = env("SECRET_KEY")

# Parse database connection url strings
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    "default": env.db(),
}


try:
    # Define you own logging in LOGGING here
    from .logging import *  # type: ignore  # pylint: disable=wildcard-import
except ImportError:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{asctime} [{levelname}] {module}: {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "scraper.log",
                "formatter": "verbose",
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": [],
            "level": "WARNING",
        },
        "loggers": {
            #'order_scraper.management.commands.scrapers.......'
            #'order_scraper.management.commands....'
            "hlo.management.commands": {
                #"handlers": ["console", "file"],
                "handlers": ["console"],
                "level": "DEBUG",  # Will be overriden by --verbosity
            }
        },
    }


ALLOWED_HOSTS: List[str] = env.list("ALLOWED_HOSTS")

STATIC_URL: str = env("STATIC_URL")

INSTALLED_APPS: List[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djmoney",  # MoneyField
    "haystack",
    "rest_framework",
    "django_filters",
    "django_bootstrap_icons",
    "django_extensions",
    "taggit",
    "django_bootstrap5",
    "django_select2",
    "debug_toolbar",
]

INSTALLED_APPS += env.list("INSTALLED_APPS", default=[])

MIDDLEWARE: List[str] = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
]

ROOT_URLCONF: str = "hlo.urls"

TEMPLATES: List[Dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (Path(BASE_DIR, "hlo", "templates")),
        ],
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

WSGI_APPLICATION: str = "hlo.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": env("PASSWORD_MIN_LEN"),
        },
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

BOOTSTRAP5 = { # We need bootstrap >= 5.3 for dark mode
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "integrity": "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin": "anonymous",
    },
    "javascript_url": { 
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous",
    },
}

# run `python ./manage.py graph_models` to update hlo_model_graph.png
GRAPH_MODELS = {
  'group_models': True,
  'app_labels': ["hlo"],
  'exclude_models': ["ColorTagBase","GenericTaggedItemBase","TagBase"],
  'output': "hlo_model_graph.png",
  "color_code_deletions": True,
  "arrow_shape": "normal",
  "rankdir": "TB",
  "theme": "django2018",
}