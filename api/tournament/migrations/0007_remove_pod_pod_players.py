# Generated by Django 3.0.8 on 2020-10-07 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20201007_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pod',
            name='pod_players',
        ),
    ]
