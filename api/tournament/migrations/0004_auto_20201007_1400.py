# Generated by Django 3.0.8 on 2020-10-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_auto_20201006_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
