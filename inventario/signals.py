# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto, InventarioBodega
from django.core.management import call_command
from django.core.signals import request_started
from django.contrib.sessions.models import Session

def clear_sessions(sender, **kwargs):
    Session.objects.all().delete()

request_started.connect(clear_sessions)
