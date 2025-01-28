from django.apps import AppConfig


class AiModConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_mod'

    def ready(self):
        import ai_mod.signals
