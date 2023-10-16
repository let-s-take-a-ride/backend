from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import CustomUser

user = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)

admin.site.register(CustomUser, CustomUserAdmin)
