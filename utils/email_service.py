from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_template_email(user, user_agent, ip_address, template_name):
    subject = 'My Site'
    html_message = render_to_string(template_name, {
        'user': user,
        'user_agent': user_agent,
        'ip_address': ip_address
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)