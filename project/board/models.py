from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('board')


class Post(models.Model):
    postAuthor = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = RichTextUploadingField(blank=True, null=True)

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):  # чтобы перебрасывало на страницу созданного поста
        return f'/board/{self.id}'




class Reaction(models.Model):
    rPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    rUser = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField('Отклик')
    dateCreation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, blank=True, verbose_name='принято')

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        ordering = ['-dateCreation']

    def __str__(self):
        return f'{self.text}'



class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.code}'

# Create your models here.
