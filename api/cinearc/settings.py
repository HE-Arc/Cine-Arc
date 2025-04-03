import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Django secret key (retrieved from .env)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Debug mode (should be disabled in production)
DEBUG = os.getenv("DEBUG") == "True"

# Allowed hosts for the application
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "cine-arc.k8s.ing.he-arc.ch").split(",")

# Installed Django applications
INSTALLED_APPS = [
    "django.contrib.admin",  # Admin interface
    "django.contrib.auth",  # Authentication system
    "django.contrib.contenttypes",  # Content type framework
    "django.contrib.sessions",  # Session framework
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static files handling
    "cinearcapp",  # Custom app
    "rest_framework",  # Django REST framework
    'rest_framework_simplejwt',  # JWT authentication
    "corsheaders",  # CORS headers handling
    "celery",  # Celery for task queue
    "django_celery_beat",  # Celery periodic task scheduler
]

# REST framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT-based authentication
    ),
}

# JWT configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Access token validity
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh token validity
    "ROTATE_REFRESH_TOKENS": True,  # Rotate refresh tokens on use
    "BLACKLIST_AFTER_ROTATION": True,  # Blacklist old tokens after rotation
    "AUTH_HEADER_TYPES": ("Bearer",),  # Token prefix in headers
}

# Middleware configuration
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Handle CORS
    "django.middleware.security.SecurityMiddleware",  # Security enhancements
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session management
    "django.middleware.common.CommonMiddleware",  # Common HTTP middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentication middleware
    "django.contrib.messages.middleware.MessageMiddleware",  # Messaging middleware
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]

# CORS configuration to allow frontend access
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Local development
    "http://127.0.0.1:5173",  # Alternative local address
    "https://cine-arc.k8s.ing.he-arc.ch",  # Production URL
]

# Root URL configuration
ROOT_URLCONF = "cinearc.urls"

# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Template engine
        "DIRS": [],  # Custom template directories
        "APP_DIRS": True,  # Enable app-specific templates
        "OPTIONS": {
            "context_processors": [  # Context processors for templates
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application configuration
WSGI_APPLICATION = "cinearc.wsgi.application"

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Default SQLite database
        'NAME': BASE_DIR / 'db.sqlite3',  # SQLite database file
    },
    "server": {
        "ENGINE": "django.db.backends.postgresql",  # PostgreSQL database
        "NAME": os.getenv("POSTGRES_DB"),  # Database name
        "USER": os.getenv("POSTGRES_USER"),  # Database user
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # Database password
        "HOST": os.getenv("POSTGRES_HOST"),  # Database host
        "PORT": os.getenv("POSTGRES_PORT"),  # Database port
    }
}

# Password validation configuration
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # Prevent passwords similar to user attributes
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # Enforce minimum password length
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # Prevent common passwords
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # Prevent fully numeric passwords
]

# Language and timezone configuration
LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Paris")  # Default timezone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# Static files configuration
STATIC_URL = "/static/"  # URL for serving static files
STATIC_ROOT = BASE_DIR / "static"  # Directory for collected static files

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery configuration for task queue
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")  # Redis broker URL
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")  # Redis result backend
CELERY_ACCEPT_CONTENT = ["json"]  # Accepted content types
CELERY_TASK_SERIALIZER = "json"  # Task serialization format
CELERY_SEND_EVENTS = True  # Enable event sending
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"  # Scheduler for periodic tasks
