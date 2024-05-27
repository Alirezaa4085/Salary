# utils/email_service.py

from django.core.mail import send_mail
from django.conf import settings

def send_email(subject: str, message: str, recipient_list: list[str]):
#TODO: use templates for this method    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import traceback


def send_emailtemplate(subject, to, context, template_name):
    try:
        html_message = render_to_string(template_name, context)
        print('html_message')
        print(html_message)
        plain_message = strip_tags(html_message)
        print('plain_message')
        print(plain_message)
        from_email = settings.EMAIL_HOST_USER
        print('from_email')
        print(from_email)
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        print('ok')
    except:
        print(traceback.format_exc())
        pass