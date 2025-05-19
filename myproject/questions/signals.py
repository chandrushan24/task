import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import TestModel

@receiver(post_save, sender=TestModel)
def signal_handler(sender, instance, **kwargs):
    print("🔔 Signal triggered")
    print("Thread ID (signal):", threading.get_ident())

    # Transaction rollback check
    if instance.name == 'raise':
        raise Exception("Force rollback from signal")
