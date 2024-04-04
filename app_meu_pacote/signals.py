# app_meu_pacote/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Encomenda

@receiver(post_save, sender=Encomenda)
def enviar_email_pos_criacao(sender, instance, created, **kwargs):
    if created:
        # Lógica para enviar email notificando sobre a nova encomenda
        pass
