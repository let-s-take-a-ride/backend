from django.contrib import admin
from .models import Event, EventMembership

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date', 'average_speed', 'max_members')
    list_filter = ('date', 'average_speed')
    search_fields = ('name', 'owner__username')
    date_hierarchy = 'date'

@admin.register(EventMembership)
class EventMembershipAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'joined_at')
    list_filter = ('event__date', 'event__average_speed')
    search_fields = ('event__name', 'user__username')
    date_hierarchy = 'joined_at'
