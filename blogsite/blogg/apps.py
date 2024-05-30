# blogg/apps.py
from django.apps import AppConfig

class BloggConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogg'

    def ready(self):
        import blogg.signals  # Import the signals module
