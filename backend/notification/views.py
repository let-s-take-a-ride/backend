from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets, permissions, filters, serializers, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

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