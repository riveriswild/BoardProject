# Generated by Django 3.2.6 on 2021-09-02 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_reaction_rpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reaction',
            options={'ordering': ['-dateCreation'], 'verbose_name': 'Отклик', 'verbose_name_plural': 'Отклики'},
        ),
    ]