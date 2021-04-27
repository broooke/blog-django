from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config.celery import app
from .models import Mailing, Article


@app.task
def mailing():
    for mail in Mailing.objects.all():
        template = render_to_string('extends/email_dict.html', {
            'articles': Article.objects.all().order_by('date')[:3],
        })

        text_content = strip_tags(template)

        email = EmailMultiAlternatives(
            "Еженедельные обновления",
            text_content,
            settings.EMAIL_HOST_USER,
            [mail.email],
        )

        email.attach_alternative(template, "text/html")
        email.send()