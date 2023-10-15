from django.urls import path
from .views import TestAuthenticationView

urlpatterns = [
    path('test-auth/', TestAuthenticationView.as_view(), name='test-auth'),
]
