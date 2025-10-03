# Air Quality App Configuration

from django.apps import AppConfig


class AirQualityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'air_quality'
    verbose_name = 'Air Quality Management'
    
    def ready(self):
        """Initialize app when Django starts"""
        try:
            # Import signals if any
            import air_quality.signals
        except ImportError:
            pass