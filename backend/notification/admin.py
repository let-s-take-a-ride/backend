from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user', 'user__nickname')
    date_hierarchy = 'created_at'


