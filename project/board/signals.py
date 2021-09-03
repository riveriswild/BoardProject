from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Reaction



@receiver(post_save, sender=Reaction)
def new_reply(sender, instance, created, **kwargs):
    post_author = instance.rPost.postAuthor  # автор поста
    email = post_author.user.email     # мейл автора поста
    username = post_author.user.username  # юзернейм автора поста
    r_username = instance.rUser.user.username # юм автора отклика
    post = instance.rPost  # пост
    r_author = instance.rUser # автор отклика


    if created:
        html_content = render_to_string(
            'new_reaction.html',
            {
                'text': instance.text,
                'username': username,
                'rUsername': r_username,
                'link': f'http://127.0.0.1:8000/reactions',
                'post': post,
            })
        msg = EmailMultiAlternatives(
            subject=f' Привет, {username}',
            from_email='riveriswild.rw@gmail.com',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    else:
        if instance.accepted:
            html_content = render_to_string(
                'reaction_accepted.html',
                {
                    'text': instance.text,
                    'username': username,
                    'rUsername': r_username,
                    'link': f'http://127.0.0.1:8000/my_reactions',
                    'post': post,
                })
            msg = EmailMultiAlternatives(
                subject=f' Привет, {r_username}',
                from_email='riveriswild.rw@gmail.com',
                to=[r_author.user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()







