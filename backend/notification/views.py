from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets, permissions, filters, serializers, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['user', 'created_at', 'is_read']
    search_fields = ['user__id', 'message']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(user__id__icontains=search) |
                Q(message__icontains=search)
            )
        return queryset

    @action(detail=False, methods=['get'], url_path='user-notifications/(?P<user_id>\d+)',)
    def user_notifications(self, request, user_id=None):
        if not user_id:
            return Response({"message": "User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        notifications = Notification.objects.filter(user__id=user_id).order_by('-created_at')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)