import django_filters
from django.forms import DateInput
from django import forms
from .models import Post, Category, Reaction


class ReactionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='dateCreation', widget=DateInput(attrs={'type': 'date'}),
                                     label='Дата создания отклика:')

    class Meta:
        model = Reaction
        fields = {'rPost'}
