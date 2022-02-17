# Generated by Django 4.0.1 on 2022-01-31 14:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_event_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration_hours',
        ),
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 31, 14, 49, 10, 417353, tzinfo=utc)),
            preserve_default=False,
        ),
    ]