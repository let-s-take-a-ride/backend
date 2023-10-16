from django.urls import path
from .views import LoginView  # Upewnij się, że importujesz LoginView z właściwego modułu

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
