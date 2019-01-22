from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from twitter_app.models import EmailVerification

User = get_user_model()

@shared_task
def test_task(a, b):
    time.sleep(5)
    return a + b


@shared_task
def email_verification(user_id):
    user = User.objects.filter(pk=user_id).last()
    if user:
        verification = EmailVerification.objects.create(
            user=user
        )
        subject, from_email, to = 'Email verification', settings.EMAIL_HOST_USER, user.email
        text_content = 'This is an important message.'
        html_content = '<p>Please verify yourself. <a href="{}">Here</a></p>'.format("http://localhost:8000" + verification.get_verification_url())
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return "Email successfuly send to {}".format(user.email)