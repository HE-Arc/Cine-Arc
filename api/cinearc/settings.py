import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Chemin du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète Django (récupérée depuis .env)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Mode debug (désactivé en production)
DEBUG = os.getenv("DEBUG") == "True"

# Définir les hôtes autorisés
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "cine-arc.k8s.ing.he-arc.ch").split(",")

# Applications Django installées
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cinearcapp",
    "rest_framework",
    "corsheaders",
    "celery",
    "django_celery_beat",
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuration CORS pour autoriser le frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Développement local
    "http://127.0.0.1:5173",  # Adresse alternative en local
    "https://cine-arc.k8s.ing.he-arc.ch",  # URL de production
]

# Fichier des URLs racine
ROOT_URLCONF = "cinearc.urls"

# Configuration des templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Configuration WSGI
WSGI_APPLICATION = "cinearc.wsgi.application"

# Configuration de la base de données (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    "server": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "cine_arc"),  # Nom de la DB
        "USER": os.getenv("POSTGRES_USER", "cine_arc"),  # Utilisateur
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "Ky9eh46KuJftmgygzrnoozehk"),  # Mot de passe
        "HOST": os.getenv("POSTGRES_HOST", "postgres-service"),  # Service PostgreSQL (Docker/K8s)
        "PORT": os.getenv("POSTGRES_PORT", "5432"),  # Port PostgreSQL
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Configuration de la langue et du fuseau horaire
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Paris")
USE_I18N = True
USE_TZ = True

# Fichiers statiques (CSS, JS, images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Clé primaire par défaut
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuration Celery avec Redis
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_SEND_EVENTS = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
