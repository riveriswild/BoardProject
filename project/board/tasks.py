from celery import shared_task
from datetime import timezone, datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Profile

@shared_task
def weekly_email():
    timer = datetime.now(timezone.utc)
    for user in Profile.objects.all():
        email = user.user.email
        posts = Post.objects.filter(dateCreation__gte=(timer - timedelta(days=7)))
        html_content = render_to_string(
            'weekly_posts.html',
            {
                'username': user.user.username,
                'posts': posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Посты за неделю',
            from_email='riveriswild.rw@gmail.com',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
