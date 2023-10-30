from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_events')
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='event_photos/', blank=True, null=True)
    average_speed = models.FloatField()
    members_count = models.PositiveIntegerField(default=0)
    max_members = models.PositiveIntegerField()
    date = models.DateField()
    gpx_track = models.FileField(upload_to='gpx_tracks/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.name

    def can_add_member(self):
        return self.memberships.count() < self.max_members

    def update_members_count(self):
        self.members_count = self.memberships.count()
        self.save()


class EventMembership(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.username} in {self.event.name}'


