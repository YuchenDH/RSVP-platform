# Generated by Django 2.0.2 on 2018-02-10 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0006_auto_20180210_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='userspecify',
            field=models.BooleanField(default=0),
        ),
    ]
