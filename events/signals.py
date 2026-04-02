from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import EventRegistration


@receiver(post_save, sender=EventRegistration)
def send_registration_email(sender, instance, created, **kwargs):
    if not created:
        return

    event = instance.event
    user = instance.user

    if not user.email:
        return

    send_mail(
        subject=f"Registration confirmed: {event.title}",
        message=(
            f"Hi {user.username},\n\n"
            f"You are registered for event '{event.title}'.\n"
            f"Date: {event.date}\n"
            f"Location: {event.location}\n\n"
            "Thanks for using Event Management API."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
