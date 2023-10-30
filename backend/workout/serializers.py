from rest_framework import serializers
from .models import Event, EventMembership



class EventMembershipSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='event.name')
    user_username = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = EventMembership
        # fields = '__all__'
        fields = ['event_name', 'user_username', 'joined_at', 'event', 'user']

class EventSerializer(serializers.ModelSerializer):
    memberships = EventMembershipSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        # fields = '__all__'
        fields = ['id', 'name', 'description', 'memberships', 'owner', 'date', 'average_speed', 'members_count', 'max_members', 'city', 'photo', 'gpx_track']

