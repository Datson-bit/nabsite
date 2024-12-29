from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import random
from .models import EventPass
import string 


def send_registration_email(user_email, event_name):
    subject = f"Registration Confirmation for {event_name}"
    message = f"Thank you for registering for {event_name}!"
    html_message = render_to_string('emails/registration_email.html', {'event_name': event_name})
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
        html_message=html_message,
    )


def generate_unique_pass_code():
    while True:
        pass_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not EventPass.objects.filter(pass_code=pass_code).exists():
            return pass_code

