# Generated by Django 3.1 on 2020-09-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='signup_confirmation',
            field=models.BooleanField(default=False),
        ),
    ]
