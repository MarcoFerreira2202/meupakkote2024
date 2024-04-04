from django.apps import AppConfig


class AppMeuPacoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_meu_pacote'

# app_meu_pacote/apps.py
    def ready(self):
        import app_meu_pacote.signals  # Importa os sinais
