from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, EventRegistration


class EventApiTests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username="organizer", password="Password123")
        self.attendee = User.objects.create_user(username="attendee", password="Password123")

        self.event = Event.objects.create(
            title="Python Meetup",
            description="Django API meetup",
            date=timezone.now() + timedelta(days=3),
            location="Online",
            organizer=self.organizer,
        )

    def _auth(self, username, password):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": username, "password": password},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_register_to_event(self):
        self._auth("attendee", "Password123")
        url = reverse("event-register", kwargs={"pk": self.event.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventRegistration.objects.filter(event=self.event, user=self.attendee).count(), 1)

    def test_non_organizer_cannot_update_event(self):
        self._auth("attendee", "Password123")
        url = reverse("event-detail", kwargs={"pk": self.event.id})

        response = self.client.patch(url, {"title": "Hacked"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

