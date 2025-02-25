# Dockerfile
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installer pipenv
RUN pip install pipenv

# Copier les fichiers de dépendances
COPY Pipfile Pipfile.lock /app/

# Installer les dépendances
RUN pipenv install --system

# Copier le reste de l’application
COPY . /app/

# Exposer le port de Django
EXPOSE 8000

# Commande par défaut
CMD ["sh", "-c", "python manage.py migrate && python manage.py migrate django_celery_beat && python manage.py runserver 0.0.0.0:8000"]