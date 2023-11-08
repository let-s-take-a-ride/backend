from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .authentication import Auth0TokenAuthentication
from notification.models import Notification
import urllib.parse

class LoginView(APIView):
    authentication_classes = [Auth0TokenAuthentication]

    def post(self, request, format=None):
        user = request.user

        decoded_url = urllib.parse.unquote(user.picture.url[7:]) if user.picture else None
        corrected_url = decoded_url.replace("https:/", "https://")
        print(user.__dict__)

        if user.is_authenticated:
            unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

            data = {
                'id': user.id,
                'username': user.nickname,
                'email': user.email,
                'picture': corrected_url,
                'is_first_login': user.first_login,
                'notifications_count': unread_notifications

            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid authentication credentials'}, status=status.HTTP_401_UNAUTHORIZED)
