from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUser, UserPreferences

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]


admin.site.register(CustomUser, CustomUserAdmin)


class UserPreferencesAdmin(admin.ModelAdmin):
    # Add any custom configurations for the UserPreferences model here
    list_display = ('user', 'distance', 'average', 'city')

# Register the UserPreferences model with the UserPreferencesAdmin class
admin.site.register(UserPreferences, UserPreferencesAdmin)
