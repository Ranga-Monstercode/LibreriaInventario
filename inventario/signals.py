# myapp/signals.py
from django.core.management import call_command
from django.core.signals import request_started
from django.contrib.sessions.models import Session

def clear_sessions(sender, **kwargs):
    Session.objects.all().delete()

request_started.connect(clear_sessions)
