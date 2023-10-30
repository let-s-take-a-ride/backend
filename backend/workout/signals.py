from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import EventMembership
@receiver([post_save, post_delete], sender=EventMembership)
def update_event_members_count(sender, instance, **kwargs):
    event = instance.event
    event.members_count = event.memberships.count()
    event.save()
