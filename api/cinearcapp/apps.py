from django.apps import AppConfig

# Configuration class for the 'cinearcapp' Django application
class CinearcappConfig(AppConfig):
    # Specifies the default type of primary key field for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    # Defines the name of the application
    name = 'cinearcapp'
