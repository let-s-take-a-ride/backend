from rest_framework import viewsets, permissions, filters, serializers
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, EventMembership
from .serializers import EventSerializer, EventMembershipSerializer
import django_filters
from rest_framework.response import Response

from django.db.models import Q
from rest_framework.decorators import action


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['name', 'date', 'average_speed', 'members_count', 'max_members']
    search_fields = ['name', 'owner__nickname', 'city']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search) |
                Q(owner__nickname__icontains=search)
            )
        return queryset

    @action(detail=False, methods=['get'])
    def hosting(self, request, *args, **kwargs):
        # print(request.user + " authenticated userr")
        events = Event.objects.filter(owner=request.user)
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def attending(self, request, *args, **kwargs):
        memberships = EventMembership.objects.filter(user=request.user).exclude(event__owner=request.user)
        events = Event.objects.filter(id__in=memberships.values_list('event_id', flat=True))
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        # serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.update_members_count()


class EventMembershipViewSet(viewsets.ModelViewSet):
    queryset = EventMembership.objects.all()
    serializer_class = EventMembershipSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    search_fields = ['event__name', 'user__nickname']
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsEventOwnerOrReadOnly]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        if event.can_add_member():
            # serializer.save(user=self.request.user)
            serializer.save()
        else:
            raise serializers.ValidationError("Maximum members limit reached for this event.")

