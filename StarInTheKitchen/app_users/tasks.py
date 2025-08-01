from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_email_to_new_registered_user(email, full_name):
    email_context = {
        'full_name': full_name,
    }

    subject = '👋 Welcome to Star in the Kitchen!'
    to_email = email
    recipient_list = [to_email]
    template_name = 'emails/welcome_to_star_in_the_kitchen.html'
    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=email_context
    )
    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=convert_to_html_content,
        fail_silently=True
    )