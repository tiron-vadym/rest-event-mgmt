from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event, EventRegistration
from events.permissions import IsOrganizerOrReadOnly
from events.serializers import EventRegistrationSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("organizer").all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filterset_fields = ["organizer", "date"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["date", "created_at", "title"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        registration, created = EventRegistration.objects.get_or_create(user=request.user, event=event)
        if not created:
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], permission_classes=[permissions.IsAuthenticated])
    def unregister(self, request, pk=None):
        event = self.get_object()
        registration = get_object_or_404(EventRegistration, user=request.user, event=event)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def attendees(self, request, pk=None):
        event = self.get_object()
        registrations = event.registrations.select_related("user").all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
