from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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
