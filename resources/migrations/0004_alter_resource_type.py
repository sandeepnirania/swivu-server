# Generated by Django 4.0.1 on 2022-01-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_resource_type_alter_resource_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Person'), (2, 'Equipment'), (3, 'Vehicle')], default=1, verbose_name='resource type'),
        ),
    ]