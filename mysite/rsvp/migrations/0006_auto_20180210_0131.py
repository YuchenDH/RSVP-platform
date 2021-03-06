# Generated by Django 2.0.2 on 2018-02-10 01:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rsvp', '0005_auto_20180207_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='original',
            field=models.BooleanField(default=True, help_text='Is the option added by owner?'),
        ),
        migrations.AddField(
            model_name='option',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_and_time',
            field=models.DateTimeField(help_text='Enter the date and time of the event as yyyy-mm-dd 23:59'),
        ),
    ]
