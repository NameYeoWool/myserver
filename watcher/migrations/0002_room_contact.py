# Generated by Django 2.2 on 2019-04-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='contact',
            field=models.BooleanField(default=False, help_text='가맹점 입니까?'),
        ),
    ]
