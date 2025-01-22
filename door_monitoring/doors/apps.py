from django.apps import AppConfig


class DoorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doors"

    def ready(self):
        from .mqtt_client import start_mqtt_client
        start_mqtt_client()