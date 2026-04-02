from django.utils import timezone
from rest_framework import serializers

from events.models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source="organizer.username", read_only=True)
    registered_users_count = serializers.IntegerField(source="registrations.count", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "organizer_username",
            "registered_users_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("organizer", "created_at", "updated_at")

    @staticmethod
    def validate_date(value):
        if value <= timezone.now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value


class EventRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = EventRegistration
        fields = ("id", "user", "username", "event", "registered_at")
        read_only_fields = ("user", "event", "registered_at")
