# Generated by Django 4.0.1 on 2022-01-31 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_board_options'),
        ('tasks', '0002_alter_task_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)ss', to='boards.board', verbose_name='board'),
        ),
    ]
