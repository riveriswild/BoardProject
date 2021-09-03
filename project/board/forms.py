from django import forms
from django.forms import ModelForm
from .models import Post, Reaction
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# форма добавления нового поста
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'postCategory', 'text']
        labels = {
            'title': 'Заголовок',
            'postCategory': 'Категория',
            'text': 'Текст',
        }
        widgets = {'text': CKEditorWidget}


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class ReactionForm(ModelForm):
    class Meta:
        model = Reaction
        fields = ['text']
        labels = {
            'text': 'Текст',
        }
