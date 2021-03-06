# Generated by Django 4.0.1 on 2022-01-31 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0002_alter_board_options'),
        ('events', '0003_remove_event_resource'),
        ('resources', '0004_alter_resource_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', to='boards.board', verbose_name='business')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.resource')),
            ],
            options={
                'verbose_name': 'assignment',
            },
        ),
    ]
