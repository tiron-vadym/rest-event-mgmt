from django.contrib import admin

from events.models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "organizer")
    list_filter = ("date", "location")
    search_fields = ("title", "description", "location", "organizer__username")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "registered_at")
    list_filter = ("registered_at",)
    search_fields = ("event__title", "user__username", "user__email")
