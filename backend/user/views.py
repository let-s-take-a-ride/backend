from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets
from .models import CustomUser, UserPreferences
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
class TestAuthenticationView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Hello!'})



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@api_view(['POST'])
def update_preferences(request):
    user = request.user
    data = request.data
    if user.is_authenticated:
        preferences, created = UserPreferences.objects.get_or_create(user=user)
        for field, value in data.items():
            setattr(preferences, field, value)
        preferences.save()
        user.is_first_login = False
        user.save()
        return Response({'status': 'preferences updated'})
    return Response({'error': 'Not authenticated'}, status=401)